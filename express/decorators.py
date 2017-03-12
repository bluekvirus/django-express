"""
Express decorators for decorating service functions and models as RESTful apis;

@author Tim Lauv
@created 2017.01.19
"""
from functools import wraps
from django.views.decorators.http import require_http_methods, require_safe
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.db.models import Model as DjangoModel
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.http import Http404
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
	def decorator(funcOrModel):
		"""
		This should be wrapping on @service, @serve* wrapped functions/models

		@url('/foo/bar') will mount service without app name in the path
		@url('foo/bar') will mount with app name before this path

		Note that @url() will replace the service default entrypoint
		Note that @url() can be applied multiple times
		"""
		if type(funcOrModel) is DjangoModel:
			tartget = funcOrModel
		else:
			@wraps(funcOrModel)
			def wrapper(req, *args, **kwargs):
				return funcOrModel(req, *args, **kwargs)
			target = wrapper
		
		# this will be used later in autodiscover()
		target._url = funcOrModel._url + [path] if type(funcOrModel._url) is list else [path]
		return target
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
	wrapper.__name__ = func.__name__
	wrapper.__doc__ = func.__doc__
	wrapper.__module__ = func.__module__
	# base entrypoint <full module path without app name>/<func>
	wrapper._url = '/'.join(func.__module__.split('.')[1:] + [func.__name__])
	return wrapper


# use only on a Django ORM Model cls
def serve(Model):
	"""
	Serve a Model with default CRUD ops mapped to RESTful apis.
	Make sure this is the first/closest @wrapper on your models.

	Note this one has csrf protection enabled.
	"""
	return _serve_model()(Model)


def serve_unprotected(Model):
	"""
	Same as @serve but without csrf protection.
	"""
	return _serve_model(enable_csrf=False)(Model)


# private worker fn for @serve*
def _serve_model(enable_csrf=True):
	"""
	DO NOT USE THIS ONE DIRECTLY AS MODEL CLASS DECORATOR!

	Create default CRUD op to APIs mapping.

	Note that unlike @service we do the url-->fn() reg here.
	Warning: no validation yet...
	Warning: no pagination yet...
	Warning: no filter/sort support yet...
	"""
	def decorator(Model):
		
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
			#variable indicates whether page_query in error or not
			page_error = False

			#get field, indicates shows what field after query. ?field=foo,bar
			field = req.params.get('field', None)
			if(field):#trim field from string to a list for being used in value_list(), if exists.
				field = field.split(',')

			#check whether single query or not
			if req.params.get('id', None):
				result = Model.objects.filter(**dict({'id': req.params['id']}))

			#multiple query. filt and sort first, then paging
			else:
				#get filter parameter, ?filter=foo1:bar1&filter=foo2:bar2
				filt = req.GET.getlist('filter')
				if(filt): #make filt into an dicitionary to pass into Model.objects.filter, if exists.
					filt = dict(e.split(':') for e in filt)

				#get sort parameter ?sort=foo, -bar
				sort = req.params.get('sort', None)
				if(sort):#trim sort from string to a list for being used in order_by, if exists.
					sort = sort.split(',')

				#get how many items on one page ?size=number
				size = int(req.params.get('size', 0))
				
				#get which index to start paging ?offset=number
				offset = int(req.params.get('offset', 0))

				#get which page does user acquire ?page=number
				page = int(req.params.get('page', 1))

				#filter and sort exists at the same time
				if(filt and sort):
					#filt and then sort
					result = Model.objects.filter(**filt).order_by(*sort)
				#only filter
				elif(filt):
					result = Model.objects.filter(**filt)
				#only sort
				elif(sort):
					result = Model.objects.order_by(*sort)
				#no filt and sort
				else:
					result = Model.objects.all()

				#paging, only paging when size, offset and page are all valid
				if((size > 0) and (offset >= 0) and (page > 0)):
					#check whether offset is within the length of the result, it has enough pages to display
					if((offset < result.count()) and ((result.count() - offset) / size > page - 1 )):
						#truncate result
						result = result[offset:]
						#generate return result
						p = Paginator(result, size)
						result = p.page(page).object_list
					else:
						page_error = True

			#return result
			if(page_error):
				res.json({
					'payload': '!!page query error!!'
					})
			elif(not len(result) and req.params.get('id', None)):
				raise Http404('No %s matches the given query.' % result.model._meta.object_name)
			else:
				res.json({
					'payload': list(result.values(*field if field else [])),
					'count': result.count()
					})
				
		@methods('PUT', 'PATCH')
		@service
		def update(req, res, *args, **kwargs):
			pk = req.json.get('payload', {}).get('id', None)
			m = get_object_or_404(Model, pk=pk)
			for k, v in req.json['payload'].items():
				setattr(m, k, v)
			m.save()
			res.json({'id': m.id})

		@methods('DELETE')
		@service
		def delete(req, res, *args, **kwargs):
			pk = req.params.get('id', None)
			m = get_object_or_404(Model, pk=pk)
			noe, tinfo = m.delete()
			res.json({'affected': tinfo})

		# Warning: 'HEAD' reply body may be ignored by some browser (so use headers only)
		@methods('HEAD')
		@service
		def headcount(req, res, *args, **kwargs):
			res['X-Django-App-Model'] = Model.__module__ + '.' + Model.__name__
			res['X-DB-Table-Count'] = Model.objects.count()
			#res.json({'model': Model.__module__ + '.' + Model.__name__, 'count': Model.objects.count()})


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
			'DELETE': delete,
		}

		@csrf_exempt
		def dispatcher(req, *args, **kwargs):
			fn = mapping.get(req.method, nosupport)
			if enable_csrf:
				fn = csrf(fn)
			#if enable_permissions:
			# 	...
			return fn(req, *args, **kwargs)

		Model._express_dispatcher = dispatcher
		Model._url = Model.__module__.replace('.', '/') + '/' + Model.__name__
		return Model

	return decorator
