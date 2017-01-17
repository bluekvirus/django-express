# from django.http import HttpRequest, HttpResponse
from express.decorators import inspect, service, methods, url

@methods(['GET', 'POST'])
@url('/absolute/url')
@service
def abc(req, res, *args, **kwargs):
	res.json({**req.GET, **req.POST})

@service
def efg(req, res, *args, **kwargs):
	res.html('Nothing but a test from <h2>{}</h2>'.format(__name__))

@service
def hij(req, res, *args, **kwargs):
	res.file('db.sqlite3')