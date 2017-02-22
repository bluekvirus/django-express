"""
Services autodiscover (loading) and registering.

@author Tim Lauv
@created 2017.01.19
"""
from importlib import import_module
# from django.utils.module_loading import autodiscover_modules (BUGGY: the registry `register_to` is not populated atm...)
from django.conf import settings
from django.conf.urls import url
from django.apps import apps as django_apps
import inspect
import logging

logger = logging.getLogger('django')


def autodiscover(*args):
	"""
	Automatically register tagged functions/models with urlconf.

	"""
	for app in django_apps.get_app_configs():
		for target in args:
			try:
				# load the target module from that app
				t = import_module('{}.{}'.format(app.name, target))
				services._registry[app.name] = t

				# inspect it for functions/classes
				for name, m in inspect.getmembers(t, lambda x: inspect.isfunction(x) or inspect.isclass(x)):
					# filter out non @service, @serve* 
					if(hasattr(m, '_url')):
						# override mount point by @url('path'), can be multiple
						path = m._url if type(m._url) is list else [m._url]
						for p in path:
							if not p.startswith('/'):
								# relevant path, still mount under app.name
								if not p.startswith(app.name):
									p = app.name + '/' + p
							else:
								# absolute path, mount without app.name
								p = p[1:] # remove leading '/'
							services.urls += [
								url(r'^{}$'.format(p), m if not hasattr(m, '_express_dispatcher') else m._express_dispatcher, name=m.__module__ + '.' + name)
							]
			except Exception as e:
				logger.warning('[express: autodiscover ' + app.name + '] ' + str(e))
				#pass
			
	services.global_urls = import_module(settings.ROOT_URLCONF).urlpatterns


class ServiceRegistry(object):
	"""docstring for ServiceRegistry"""

	def __init__(self):
		super().__init__()
		self._registry = {} # to be used by autodiscover_modules() (BUGGY atm)
		self.urls = []


services = ServiceRegistry()
default_app_config = 'express.apps.ExpressConfig'