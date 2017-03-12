"""
Services autodiscover (loading) and registering.

@author Tim Lauv
@created 2017.01.19
@updated 2017.03.11
"""
from importlib import import_module
from django.utils.functional import cached_property
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
		# init modules and services registery
		services._registry[app.name] = {}
		services._services[app.name] = []

		# loop within each app for each targeted modules (e.g 'services', 'models')
		for target in args:
			try:
				# load the target module from that app
				t = import_module('{}.{}'.format(app.name, target))
				services._registry[app.name][target] = t # keep a module record, but not really used atm.

				# inspect it for functions/classes
				for name, m in inspect.getmembers(t, lambda x: inspect.isfunction(x) or inspect.isclass(x)):
					# filter out non @service, @serve* 
					if(hasattr(m, '_url')):
						# override mount point by @url('path'), can be multiple
						path = m._url if type(m._url) is list else [m._url]
						for p in path:
							services._services[app.name].append({
								# keep a service record (to generate url by calling services.urls/url() later)
								'path': p,
								'name': name,
								'src': m,
							})
			except Exception as e:
				logger.warning('[express: autodiscover ' + app.name + '] ' + str(e))
				#pass
	
	# remember for DEBUG=True logging [django: base]
	services._global_urls = import_module(settings.ROOT_URLCONF).urlpatterns


class ServiceRegistry(object):
	"""docstring for ServiceRegistry"""

	def __init__(self):
		super().__init__()
		self._registry = {} # should be used by autodiscover_modules() automatically but BUGGY atm, thus manually assigned.
		self._services = {} # stores service cards collected from memeber._url
		self._generated = [] # for DEBUG=True logging

	def _generateMountURLs(self, service, prefix=None):
		# relative path
		p = service['path']
		if not p.startswith('/'):
			if prefix and not p.startswith(prefix):
				p = '/'.join([prefix, p]) # add prefix
		# absolute path
		else:
			p = p[1:] # remove leading '/'

		return url(r'^{}$'.format(p), service['src'] if not hasattr(service['src'], '_express_dispatcher') else service['src']._express_dispatcher, name='.'.join([service['src'].__module__, service['name']]))

	@cached_property
	def urls(self):
		"""return all the urls found, with app name as relative url's prefix"""
		return self.url(*self._services.keys(), prefixedByAppName=True)

	def url(self, *args, **kwargs):
		"""return only the selected app(s)'s urls for service mounting, with no relative url app prefix by default"""
		urls = []
		for app in args:
			records = self._services.get(app, [])
			for service in records:
				urls.append(self._generateMountURLs(service, app if kwargs.get('prefixedByAppName', False) else None))

		self._generated += urls # remember for DEBUG=True logging [express: uri]
		return urls


services = ServiceRegistry()
default_app_config = 'express.apps.ExpressConfig'