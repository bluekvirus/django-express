from django.db import models
from express.decorators import serve

# Create your models here.

@serve
class Device(models.Model):
	"""docstring for Device"""
	sn = models.CharField(max_length=32)

		