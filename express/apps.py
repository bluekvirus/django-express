from django.apps import AppConfig
import logging

logger = logging.getLogger('django')

class ExpressConfig(AppConfig):
    name = 'express'

    def ready(self):
    	self.module.autodiscover('services') # auto load services.py from each (installed) app
    	for url in self.module.services.urls:
    		logger.info('[express: url] ' + str(url.regex.pattern))