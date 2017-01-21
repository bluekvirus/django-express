from functools import wraps
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from express.http import ExpressRequest, ExpressResponse

# last (top)
def inspect(func):
	'''This should be the last/outmost @wrapper on your service function'''
	@wraps(func) # so you can preserve func.__name__, __module__, __doc__ and __dict__ in the decorated version.
	def wrapper(req, *args, **kwargs):
		print('Accessing service:', req.method, func.__name__)
		return func(req, *args, **kwargs)
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

methods = require_http_methods
csrf = csrf_protect
# -----------------------------

# first (bottom)
def service(func):
	'''Make sure this is the first/closest @wrapper on your service function'''
	@csrf_exempt
	def wrapper(req, *args, **kwargs):
		response = ExpressResponse()
		request = ExpressRequest(req)
		func(request, response, *args, **kwargs) # all service functions should have this signature.
		return response._res
	wrapper.__name__ = 'service_{}'.format(func.__name__)
	wrapper.__doc__ = func.__doc__
	return wrapper