from django.apps import AppConfig
import logging
from django.apps import apps

logger = logging.getLogger('django')


class ExpressConfig(AppConfig):
    name = 'express'
    applist = []
    def ready(self):
        # auto load apis indicated by services.py, models.py from each (installed) app
        self.module.autodiscover('services', 'models')
        for url in self.module.services._generated:
            logger.info('[express: uri] ' + str(url.regex.pattern) + ' -- (name: ' + str(url.name) + ')')
        for root in self.module.services._global_urls:
            logger.info('[django: base] ' + str(root.regex.pattern))

        for app in apps.get_app_configs():
            logger.debug(app.verbose_name)
            if not app.name.startswith('django'):
                self.applist.append({'vname': app.verbose_name, 'mkey': app.name})
