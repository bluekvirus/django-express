from django.apps import AppConfig
import logging
import django

logger = logging.getLogger('django')


class ExpressConfig(AppConfig):
	name = 'express'

	def ready(self):
        # auto load apis indicated by services.py, models.py from each (installed) app
		self.module.autodiscover('services', 'models')
		if django.get_version().startswith('2'): # for version 2 of django
			for url in self.module.services._generated:
				logger.info('[express: uri] ' + str(url.pattern.regex.pattern) + ' -- (name: ' + str(url.name) + ')')
			for root in self.module.services._global_urls:
				logger.info('[django: base] ' + str(root.pattern.regex.pattern))
		elif django.get_version().startswith('1'): # for versions 1.10, 1.11
			for url in self.module.services._generated:
				logger.info('[express: uri] ' + str(url.regex.pattern) + ' -- (name: ' + str(url.name) + ')')
			for root in self.module.services._global_urls:
				logger.info('[django: base] ' + str(root.regex.pattern))
			else:
				logger.error('Error, incompatible Django version detected!')
