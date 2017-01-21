from django.apps import AppConfig
import logging

logger = logging.getLogger('django-express')

class ExpressConfig(AppConfig):
    name = 'express'

    def ready(self):
    	self.module.autodiscover('services') # auto load services.py from each (installed) app
    	logger.info('urlconf express: ' + str(self.module.services.urls))