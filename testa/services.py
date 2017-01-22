# from django.http import HttpRequest, HttpResponse
from express.decorators import inspect, service, methods, url, csrf, safe
from django.urls import reverse

@methods(['GET', 'POST'])
@url('/absolute/url')
@url('relative/abcd')
@service
def abc(req, res, *args, **kwargs):
	res.json({'json': req.json, 'link:': reverse('express:testa.abc')})

@service
def efg(req, res, *args, **kwargs):
	res.json({'params': {**req.params}, 'form': {**req.form}, 'json': req.json, 'mime': req['CONTENT_TYPE']})

@service
def hij(req, res, *args, **kwargs):
	res.file('db.sqlite3')