from django.apps import AppConfig

class ExpressConfig(AppConfig):
    name = 'express'

    def ready(self):
    	self.module.autodiscover('services') # auto load services.py from each (installed) app
    	print('urlconf global:', self.module.services.global_urls)
    	print('urlconf express:', self.module.services.urls)