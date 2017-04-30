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
from django.http import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
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
        services._services[app.name] = {}  # path dict --> methods dict

        # loop within each app for each targeted modules (e.g 'services', 'models')
        for target in args:
            try:
                # load the target module from that app
                t = import_module('{}.{}'.format(app.name, target))
                services._registry[app.name][target] = t  # keep a module record, but not really used atm.

                # note that, if t is a package, only those exposed by its __init__.py are considered.

                # inspect it for functions/classes
                for name, m in inspect.getmembers(t, lambda x: inspect.isfunction(x) or inspect.isclass(x)):
                    # filter out non @service, @serve*
                    if(hasattr(m, '_path')):
                        # override mount point by @url('path'), can be multiple
                        paths = m._path if type(m._path) is list else [m._path]
                        methods = m._methods if hasattr(m, '_methods') else ['*']
                        for p in paths:
                            mapping = services._services[app.name].get(p, {})
                            for method in methods:
                                mapping[method] = {
                                    # keep a service record (to generate url by calling services.urls/url() later)
                                    'name': name,
                                    'src': m if not hasattr(m, '_express_dispatcher') else m._express_dispatcher,
                                }
                            services._services[app.name][p] = mapping
            except Exception as e:
                logger.warning('[express: autodiscover ' + app.name + '] ' + str(e))

    # remember for DEBUG=True logging [django: base]
    services._global_urls = import_module(settings.ROOT_URLCONF).urlpatterns


class ServiceRegistry(object):
    """docstring for ServiceRegistry"""

    def __init__(self):
        super().__init__()
        self._registry = {}  # should be used by autodiscover_modules() automatically but BUGGY atm, thus manually assigned.
        self._services = {}  # stores service cards collected from memeber._path
        self._generated = []  # for DEBUG=True logging

    def _generateMountURLs(self, path, mapping, app=None):
        p = path

        @csrf_exempt  # dispatcher (view) needs to be csrf exempted
        def dispatcher(req, *args, **kwargs):
            service = mapping.get(req.method, None) or mapping.get('*', None)
            if service:
                return service['src'](req, *args, **kwargs)
            else:
                return HttpResponseNotAllowed(mapping.keys())

        # relative path
        if not p.startswith('/'):
            if app:
                p = '/'.join([app, p])  # add app name prefix in addition to 'path'

        # absolute path
        else:
            p = p[1:]  # remove leading '/'

        # support reverse() in template for <a href=...> and <form action=...>
        reversable = mapping.get('*', None) or mapping.get('GET', None) or mapping.get('POST', None)
        return url(r'^{}$'.format(p), dispatcher, name='.'.join([reversable['src'].__module__, reversable['name']]) if reversable else None)

    @cached_property
    def urls(self):
        """return all the urls found, with app name as relative url's prefix"""
        return self.url(*self._services.keys())

    def url(self, *args, **kwargs):
        """return only the selected app(s)'s urls for service mounting, use noprefix=True for exposing services directly using their names"""
        urls = []
        for app in args:
            records = self._services.get(app, {})
            for path, mapping in records.items():
                urls.append(self._generateMountURLs(path, mapping, None if kwargs.get('noprefix', False) else app))

        self._generated += urls  # for DEBUG=True logging to output [express: uri] info
        return urls


services = ServiceRegistry()
default_app_config = 'express.apps.ExpressConfig'
