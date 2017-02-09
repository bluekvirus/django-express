"""
Express decorators for decorating service functions and models as RESTful apis;

@author Tim Lauv
@created 2017.01.19
"""
from functools import wraps
from django.views.decorators.http import require_http_methods, require_safe
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.conf.urls import url as urlconf
from django.forms.models import model_to_dict
from express.http import ExpressRequest, ExpressResponse
from express import services
import logging

logger = logging.getLogger('django')


# last (top) wrap
def inspect(func):
	"""
	Meta debug info of a @service decorated function.

	Note that this should be the last/outmost @wrapper on your service function.service.
	"""
	@wraps(func) # so you can preserve func.__name__, __module__, __doc__ and __dict__ in the decorated version.
	def wrapper(req, *args, **kwargs):
		logger.info('Accessing service:' + str([args, kwargs, req.method, req.GET, req.POST, req.COOKIES, req.FILES, req.user]))
		res = func(req, *args, **kwargs)
		logger.info('Replying:' + str(res))
		return res
	return wrapper


# everything in between--------
def url(path):
	def decorator(func):
		"""
		This should be wrapping on @service wrapped functions

		@url('/foo/bar') will mount service without app name in the path
		@url('foo/bar') will mount with app name before this path

		Note that @url() will replace the service function name.
		"""
		@wraps(func)
		def wrapper(req, *args, **kwargs):
			return func(req, *args, **kwargs)
		wrapper._url = func._url + [path] if hasattr(func, '_url') else [path] # this will be used later in autodiscover('services')
		return wrapper
	return decorator


def csrf(func):
	"""
	Ensures csrf token cookie or checkes it based on request method type.
	"""
	@wraps(func)
	def wrapper(req, *args, **kwargs):
		if req.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
			return (ensure_csrf_cookie(func))(req, *args, **kwargs)
			# Default cookie by CSRF_COOKIE_NAME in settings is 'csrftoken'
			# submit back in either req.form['csrfmiddlewaretoken'] or req['X-CSRFToken']
			# the latter often used by Ajax and can be configured by CSRF_HEADER_NAME in settings
		else:
			func.csrf_exempt = False #reset csrf_exempt set by @csrf_exempt during @service
			return (csrf_protect(func))(req, *args, **kwargs) 
			# Note that we don't use requires_csrf_token() here since it was for making the 'csrf_token' tag work in django templates.
	return wrapper


def methods(*args):
	return require_http_methods(args)


# pass-through decorators
safe = require_safe

# -----------------------------


# first (bottom) wrap
def service(func):
	"""
	Make sure this is the first/closest @wrapper on your service function

	Note that this decorator tags the original function with meta and new arguments. 
	The real url-->fn() registeration happens in __init__.py autodiscover() because of @url.
	"""
	@csrf_exempt # setting wrapper.csrf_exempt = True, consulted by CsrfViewMiddleware
	def wrapper(req, *args, **kwargs):
		response = ExpressResponse()
		request = ExpressRequest(req)
		func(request, response, *args, **kwargs) # all service functions should have this signature.
		return response._res
	wrapper.__name__ = 'service_{}'.format(func.__name__)
	wrapper.__doc__ = func.__doc__
	wrapper.__module__ = func.__module__
	wrapper._url = [func.__module__.replace('.', '/') + '/' + func.__name__]
	return wrapper


# use only on a Django ORM Model cls
def serve(Model):
	"""
	Create default CRUD op to APIs mapping.

	Note that unlike @service we do the url-->fn() reg here.
	Warning: no validation yet...
	Warning: no switching on the @csrf from @serve() yet...
	Warning: no pagination yet...
	Warning: no filter/sort support yet...
	"""

	#@csrf
	@methods('POST')
	@service
	def create(req, res, *args, **kwargs):
		m = Model(**req.json.get('payload', {})) #python3.5+ unpacking list/dict
		#no validation yet
		m.save()
		res.json({'id': m.id})

	@methods('GET')
	@service
	def read(req, res, *args, **kwargs):
		if req.params.get('id', None):
			m = get_object_or_404(Model, pk=req.params['id'])
			res.json({'payload': model_to_dict(m)})
		else:
			res.json({'payload': list(Model.objects.values())})

	#@csrf
	@methods('PUT', 'PATCH')
	@service
	def update(req, res, *args, **kwargs):
		pk = req.json.get('payload', {}).get('id', None)
		m = get_object_or_404(Model, pk=pk)
		for k, v in req.json['payload'].items():
			setattr(m, k, v)
		m.save()
		res.json({'id': m.id})

	#@csrf
	@methods('DELETE')
	@service
	def delete(req, res, *args, **kwargs):
		pk = req.params.get('id', None)
		m = get_object_or_404(Model, pk=pk)
		noe, tinfo = m.delete()
		res.json({'affected': tinfo})

	@methods('HEAD')
	@service
	def headcount(req, res, *args, **kwargs):
		res.json({'model': Model.__module__ + '.' + Model.__name__, 'count': Model.objects.count()})


	@service
	def nosupport(req, res, *args, **kwargs):
		res.json({'error': req.method + ' not supported...'})
		res.status(501)

	mapping = { 
		'HEAD': headcount,
		'POST': create,
		'GET': read,
		'PUT': update,
		'PATCH': update,
		'DELETE': delete 
	}

	@csrf_exempt
	def dispatcher(req, *args, **kwargs):
		fn = mapping.get(req.method, nosupport)
		return fn(req, *args, **kwargs)

	#register the apis
	services.urls += [
		urlconf(r'^{}$'.format(Model.__module__.replace('.', '/') + '/' + Model.__name__), dispatcher, name=Model.__module__ + '.' + Model.__name__)
	]

	return Model

