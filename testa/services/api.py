# from django.http import HttpRequest, HttpResponse
from express.decorators import inspect, service, methods, url, csrf, safe
from django.urls import reverse

@methods('GET', 'POST')
@url('/absolute/url')
@url('relative/abcd')
@service
def abc(req, res, *args, **kwargs):
	res.json({'json': req.json, 'link:': reverse('express:testa.services.api.abc')})

@service
def efg(req, res, *args, **kwargs):
	res.json({
		'params': dict(req.params.lists()), # use {**req.params} in python 3.5+
		'form': dict(req.form.lists()), # use {**req.form} in python 3.5+
		'json': req.json, 
		'mime': req['CONTENT_TYPE'],
		})

@service
def hij(req, res, *args, **kwargs):
	res.file('db.sqlite3')