from functools import wraps
from django.views.decorators.http import require_http_methods, require_safe
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from express.http import ExpressRequest, ExpressResponse
import logging

logger = logging.getLogger('django')

# last (top)
def inspect(func):
	'''This should be the last/outmost @wrapper on your service function'''
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
		'''
		This should be wrapping on @service wrapped functions

		@url('/foo/bar') will mount service without app name in the path
		@url('foo/bar') will mount with app name before this path

		Note that @url() will replace the service function name.
		'''
		@wraps(func)
		def wrapper(req, *args, **kwargs):
			return func(req, *args, **kwargs)
		wrapper._url = func._url + [path] if hasattr(func, '_url') else [path] # this will be used later in autodiscover('services')
		return wrapper
	return decorator

def csrf(func):
	'''Ensures csrf token cookie or checkes it based on request method type.'''
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

methods = require_http_methods
safe = require_safe
# -----------------------------

# first (bottom)
def service(func):
	'''Make sure this is the first/closest @wrapper on your service function'''
	@csrf_exempt # setting wrapper.csrf_exempt = True, consulted by CsrfViewMiddleware
	def wrapper(req, *args, **kwargs):
		response = ExpressResponse()
		request = ExpressRequest(req)
		func(request, response, *args, **kwargs) # all service functions should have this signature.
		return response._res
	wrapper.__name__ = 'service_{}'.format(func.__name__)
	wrapper.__doc__ = func.__doc__
	return wrapper