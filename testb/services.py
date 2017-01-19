# from django.http import HttpRequest, HttpResponse
from express.decorators import inspect, service, methods, url

@service
def x(req, res, *args, **kwargs):
	res.text('Nothing but a test from {}'.format(__name__))

@url('relative/url/y-service')
@service
def y(req, res, *args, **kwargs):
	res.json({
		'data': 'Nothing but a test from {}'.format(__name__),
		'text': 123
	})
	res.header('Hello~', 'World!') # header
	res.status(201) # status

@service
def z(req, res, *args, **kwargs):
	res.download('db.sqlite3')