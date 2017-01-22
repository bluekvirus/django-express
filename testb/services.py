# from django.http import HttpRequest, HttpResponse
from express.decorators import inspect, service, methods, url, csrf, safe

@safe
@service
def x(req, res, *args, **kwargs):
	#res.text('Nothing but a test from {}'.format(__name__))
	res.text('<p>Agent: {}</p>'.format(req['HTTP_USER_AGENT']))
	res.html('<p>IP: {}</p>'.format(req['REMOTE_ADDR']))
	res.text('<p>Method: {}</p>'.format(req.header('REQUEST_METHOD')))

@inspect
@url('relative/url/y-service/articles/([0-9]{4})/([0-9]{2})/')
@service
def y1(req, res, y, m, *args, **kwargs):
	res.json({
		'data': 'Nothing but a test from {}.{}'.format(__name__, 'y1 - positional capture'),
		'text': 123,
		'year': y,
		'month': m,
	})
	res['Hello~'] = 'World!' # header
	res.status(201) # status

@url('relative/url/y-service/blogs/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/')
@csrf
@service
def y2(req, res, *args, **kwargs):
	res.json({
		'data': 'Nothing but a test from {}.{}'.format(__name__, 'y2 - named (keyword) capture'),
		'text': 123,
		'year': kwargs['year'],
		'month': kwargs['month'],
	})
	res.header('Hello~', 'World!') # header
	res.status(201) # status

@service
def z(req, res, *args, **kwargs):
	res.download('db.sqlite3')