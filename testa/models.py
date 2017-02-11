from django.db import models
from express.decorators import serve, serve_unprotected

# Create your models here.

@serve_unprotected
class Device(models.Model):
	"""docstring for Device"""
	sn = models.CharField(max_length=32)

		