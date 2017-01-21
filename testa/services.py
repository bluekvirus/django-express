# from django.http import HttpRequest, HttpResponse
from express.decorators import inspect, service, methods, url

@methods(['GET', 'POST'])
@url('/absolute/url')
@url('relative/abcd')
@service
def abc(req, res, *args, **kwargs):
	res.json(req.json)

@service
def efg(req, res, *args, **kwargs):
	res.json({**req.params, **req.form})

@service
def hij(req, res, *args, **kwargs):
	res.file('db.sqlite3')