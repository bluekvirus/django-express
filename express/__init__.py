from importlib import import_module
# from django.utils.module_loading import autodiscover_modules (BUGGY: register_to is not used atm...)
from django.conf import settings
from django.conf.urls import url
from django.apps import apps as django_apps
import inspect
import logging

logger = logging.getLogger('django-express')

def autodiscover(target):
	for app in django_apps.get_app_configs():
		try:
			# load the target module from that app
			m = import_module('{}.{}'.format(app.name, target))
			services._registry[app.name] = m

			# inspect it for functions
			for name, fn in inspect.getmembers(m, inspect.isfunction):
				# filter out non @service 
				if(fn.__name__.startswith('service_')):
					# override mount point by @url('path')
					path = fn._url if hasattr(fn, '_url') else name
					if not path.startswith('/'):
						# relevant path, still mount under app.name
						path = '{}/{}'.format(app.name, path)
					else:
						# absolute path, mount without app.name
						path = path[1:] # remove leading '/'
					services.urls += [
						url(r'^{}$'.format(path), fn)
					]
		except Exception as e:
			logger.warning(str(e))
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