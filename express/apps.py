from django.apps import AppConfig
import logging

logger = logging.getLogger('django')


class ExpressConfig(AppConfig):
    name = 'express'

    def ready(self):
        # auto load apis indicated by services.py, models.py from each (installed) app
        self.module.autodiscover('services', 'models')
        for url in self.module.services._generated:
            logger.info('[express: uri] ' + str(url.regex.pattern) + ' -- (name: ' + str(url.name) + ')')
        for root in self.module.services._global_urls:
            logger.info('[django: base] ' + str(root.regex.pattern))
