# django-express 
[![PyPI-v](https://img.shields.io/pypi/v/django-express.svg)](https://pypi.python.org/pypi/django-express) 
[![PyPI-pyv](https://img.shields.io/pypi/pyversions/django-express.svg)](https://pypi.python.org/pypi/django-express) 
[![PypI-djangov](https://img.shields.io/badge/Django-1.7%2C%201.8%2C%201.9%2C%201.10-44B78B.svg)](https://www.djangoproject.com/)

Easy Restful APIs with the Django web framework.

## Install

Download through `pip` (virtualenv -p python3.3+ .venv)
```
pip install django-express
```

Add it to your `INSTALLED_APPS` in `settings.py`
```
INSTALLED_APPS = [
  # ...
  'django.contrib.staticfiles',
  'express',
]
```

## Setup
Mount the auto-discovered services to any entry point (url) you want in `urlpatterns`
```
# proj/proj/urls.py

from django.conf.urls import url, include
from express import services

urlpatterns = [
    url(r'^api/v1/', include(services.urls)) # mount them on /api/v1/<app>/<fn>
]
```

## Add RESTful services
Create apps in your Django project **normally**, this is to sub-divide your services by app name for better maintainability. Optional though.
```
./manage.py startapp app_example
./manage.py startapp another_app_with_services
```

Add a `services.py` file in each app folder containing the service functions `fn(req, res, *args, **kwargs)` decorated with `@service`
```
# proj/app_example/services.py
from express.decorators import service, methods, url


# /api/v1/absolute/url
# /api/v1/app_example/relative/abcd

@methods(['GET', 'POST'])
@url('/absolute/url')
@url('relative/abcd')
@service
def abc(req, res, *args, **kwargs):
    res.json({'json': req.json, 'link:': reverse('express:testa.abc')})


# /api/v1/app_example/efg

@service
def efg(req, res, *args, **kwargs):
    res.json({
        'params': dict(req.params.lists()), # use {**req.params} in python 3.5+
        'form': dict(req.form.lists()), # use {**req.form} in python 3.5+
        'json': req.json, 
        'mime': req['CONTENT_TYPE'],
        })


# /api/v1/app_example/hij

@service
def hij(req, res, *args, **kwargs):
	res.file('db.sqlite3')


# /api/v1/app_example/x

@service
def x(req, res, *args, **kwargs):
    #res.text('Nothing but a test from {}'.format(__name__))
    res.text('<p>Agent: {}</p>'.format(req['HTTP_USER_AGENT']))
    res.html('<p>IP: {}</p>'.format(req['REMOTE_ADDR']))
    res.text('<p>Method: {}</p>'.format(req['REQUEST_METHOD']))


# /api/v1/app_example/relative/url/y-service/articles/2017/01/

@url('relative/url/y-service/articles/([0-9]{4})/([0-9]{2})/')
@service
def y1(req, res, y, m, *args, **kwargs):
    res.json({
        'data': 'Nothing but a test from {}.{}'.format(__name__, 'y1 - positional capture'),
        'text': 123,
        'year': y,
        'month': m,
    })
    res.header('Hello~', 'World!') # header
    res.status(201) # status


# /api/v1/app_example/z

@service
def z(req, res, *args, **kwargs):
	res.download('db.sqlite3')
```
As you can see, you can still use regex captures in `@url('..path..')` if prefered. The captured group/named group will be passed normally to your service function as positional args and keyword args. However, **You can NOT use both positioned and namged group captures in the same url!! Due to django implementation.**

## Important Note
Put `@service` as the inner-most decorator, other decorators don't have this hard requirement on ordering here. You can still use all 
the decorators from the Django web framework like `@permission_required` or `@login_required` but make sure they are all above `@service`.

## APIs

### req (ExpressRequest)
- req.params['key']
- req.json
- req.form
- req.files['name']
- req.cookies['name']
- req['HTTP-HEADER']/req.header('key')

### res (ExpressResponse)
- res.html('str')/text('str')
- res.json(dict)
- res.file('path')
- res.attach('path')/download('path')
- res.status(int)
- res.redirect('url')
- res['HTTP-HEADER']/res.header('key', val)

## Decorators

### @service
Turn your `fn(req, res, *args, **kwargs)` function into a Restful service routine. Automatically detected if present in `services.py` in any installed app.

Default mounting path: `<root>/<app name>/<fn name>`

You can change the mounting path by using the `@url()` decorator. You can also use `django.urls.reverse()` to get the service mount point by name `<app>.<fn>`.

See the **Setup** section above for mounting services root in the django `urls.py`.

### @methods(m1, m2, ...)
Allowed HTTP request methods to the service. You can also use `@safe` to allow only `GET` and `HEAD` requests.

### @url(path)
Override basic service auto-path (`/<app>/<fn>`). No need to use `r'..path..'` here, what you put in `path` will be treated as raw string automatically. Feel free to put regex group captures. **Just don't mix named and annonymous capture groups in the url path, they won't work together in django.**

You can use multiple `@url()` on the same service function.

### @csrf
Setting CSRF token cookie on `GET/HEAD` requests to the service. Checks and rejects `POST/PUT/PATCH/DELETE` requests according to their csrf token + cookie pairs.

If you want an Ajax request to be guarded by django CSRF (django.middleware.csrf.CsrfViewMiddleware) you need to `GET/HEAD` the `@csrf` decorated service first to have your CSRF cookie (named `csrftoken`) set, then `POST/PUT/PATCH/DELETE` to it with real requests including either `X-CSRFToken` in header or `csrfmiddlewaretoken` in a hidden form `<input>` field. The header or hidden field value should match the value given by the cookie.

You can change the cookie and header names but **NOT** the hidden field name in the django `settings.py`.

## Licence
Copyright 2017 Tim Lauv. 
Under the [MIT](http://opensource.org/licenses/MIT) License.
