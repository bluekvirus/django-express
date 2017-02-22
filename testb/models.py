from django.db import models
from express.decorators import serve, serve_unprotected, url

# Create your models here.

@url('/absolute/db/person')
@url('db/person')
@serve_unprotected
class Person(models.Model):
	"""docstring for Device"""
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
