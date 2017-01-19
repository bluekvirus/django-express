from django.http import HttpResponse, JsonResponse, FileResponse

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
		print('get proxied attr:', attr)
		return getattr(self._res, attr)

	def __setattr__(self, attr, val):
		'''pass through attribute assignments (e.g res.status_code)'''
		if attr in ['html', 'download', '_res']:
			print('set attr:', attr)
			return super().__setattr__(attr, val)
		else:
			print('set proxied attr:', attr)
			return setattr(self._res, attr, val)

	def __setitem__(self, key, val):
		'''
		pass through headers dict assignments (e.g res['Header-Foo'] = 'Bar')

		Note: special __FOO__ methods don't get through by __getattr__()
		'''
		print('set proxied key:', key)
		self._res[key] = val

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
		self._res = self.file(srcPath, *args, **kwargs)
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
	
	def __getattr__(self, attr):
		'''
		pass through missing attributes and methods.

		Note: delegator, called whenever an attr/method is not found
		'''
		return getattr(self._req, attr)
