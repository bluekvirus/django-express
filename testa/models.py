from django.db import models
from express.decorators import serve, serve_unprotected, url

# Create your models here.

#@url('/absolute/db/device')
#@url('db/device')
@serve_unprotected
class Device(models.Model):
	"""docstring for Device"""
	sn = models.CharField(max_length=32)
	#print self, for easier debugging
	def __str__(self):
		return str(self.id) + ' ' + str(self.sn)