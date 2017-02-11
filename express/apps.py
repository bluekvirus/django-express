from django.apps import AppConfig
import logging

logger = logging.getLogger('django')

class ExpressConfig(AppConfig):
    name = 'express'

    def ready(self):
    	# auto load apis indicated by services.py, models.py from each (installed) app
    	self.module.autodiscover('services', 'models')
    	for url in self.module.services.urls:
    		logger.info('[express: url] ' + str(url.regex.pattern) + ' -- (name: ' + url.name + ')')