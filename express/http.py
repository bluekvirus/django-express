from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import redirect
import logging, json

logger = logging.getLogger('django')

class ExpressResponse(object):
	"""docstring for ExpressResponse"""
	def __init__(self):
		super().__init__()
		self.html = self.text # alias
		self.download = self.attach # alias
		self._res = HttpResponse()

	def __getattr__(self, attr):
		'''
		pass through missing methods (e.g res.write())
		
		Note: delegator, called whenever an attr/method is not found
		'''
		return getattr(self._res, attr)

	def __setattr__(self, attr, val):
		'''pass through attribute assignments (e.g res.status_code)'''
		if attr in ['html', 'download', '_res']:
			return super().__setattr__(attr, val)
		else:
			return setattr(self._res, attr, val)

	def __setitem__(self, key, val):
		'''
		pass through headers dict assignments (e.g res['Header-Foo'] = 'Bar')

		Note: special __FOO__ methods don't get through by __getattr__()
		'''
		self._res[key] = val

	def redirect(to, permanent=False, *args, **kwargs):
		self._res = redirect(to, permanent, *args, **kwargs)

	def text(self, html, *args, **kwargs):
		'''
		@alias html
		'''
		if type(self._res) is HttpResponse: # not using isinstance() type check for exact match
			self.write(html)
		else:
			self._res = HttpResponse(html, *args, **kwargs)

	def json(self, dicT, *args, **kwargs):
		self._res = JsonResponse(dicT, *args, **kwargs)

	def file(self, path, *args, **kwargs):
		'''
		path is relevant to project root (django.conf.settings.BASE_DIR)
		'''
		self._res = FileResponse(open(path, 'rb'), *args, **kwargs)

	def attach(self, srcPath, destPath='attachment.file', *args, **kwargs):
		'''
		destPath is the attachment file name after download

		@alias download
		'''
		self.file(srcPath, *args, **kwargs)
		self._res['Content-Disposition'] = 'attachment; filename={}'.format(destPath)

	def status(self, code):
		self.status_code = code

	def header(self, key, val):
		self[key] = val


class ExpressRequest(object):
	"""docstring for ExpressRequest"""
	def __init__(self, req):
		super().__init__()
		self._req = req
		self.params = self._req.GET # alias
		self.form = self._req.POST # alias (when req has Content-Disposition: form-data; or application/x-www-form-urlencoded)
		self.files = self._req.FILES # alias
		self.cookies = self._req.COOKIES # alias

		try:
			if len(self._req.body) > 0:
		
				# Note that json de/serializer from django.core is for models.
				# we use the native json module here.
				self.json = json.loads(str(self._req.body, 'utf-8'))
			else:
				self.json = {}
		except Exception as e:
			logger.warning('[express: req.json] ' + str(e))
			self.json = '!!non-json request data, use req.form or req.files instead of req.json!!' # check self.form and self.files instead for req data

	def __getattr__(self, attr):
		'''
		pass through missing attributes and methods.

		Note: delegator, called whenever an attr/method is not found
		'''
		return getattr(self._req, attr)

	def __getitem__(self, key):
		'''
		pass through headers dict gets (e.g req['Header-Foo'] = 'Bar')

		'''
		return self._req.META[key]

	def header(self, key):
		return self[key]