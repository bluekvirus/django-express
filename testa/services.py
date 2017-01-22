# from django.http import HttpRequest, HttpResponse
from express.decorators import inspect, service, methods, url, csrf, safe

@methods(['GET', 'POST'])
@url('/absolute/url')
@url('relative/abcd')
@service
def abc(req, res, *args, **kwargs):
	res.json(req.json)

@service
def efg(req, res, *args, **kwargs):
	res.json({'params': {**req.params}, 'form': {**req.form}, 'json': req.json, 'mime': req['CONTENT_TYPE']})

@service
def hij(req, res, *args, **kwargs):
	res.file('db.sqlite3')