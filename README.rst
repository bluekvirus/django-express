django-express
==============

|PyPI-v| |PyPI-pyv| |PypI-djangov|

Easy Restful APIs with the Django web framework.

Install
-------

Download through ``pip`` (virtualenv -p python3.3+ .venv)

::

    pip install django-express

Add it to your ``INSTALLED_APPS`` in ``settings.py``

::

    INSTALLED_APPS = [
      # ...
      'django.contrib.staticfiles',
      'express',
    ]

Setup
-----

Mount the auto-discovered services to any entry point (url) you want in
``urlpatterns``

::

    # proj/proj/urls.py

    from django.conf.urls import url, include
    from express import services

    urlpatterns = [
        url(r'^api/v1/', include(services.urls)) # mount everything
        url(r'^app-name/api/v1/', include(services.url('app-name', ...))) # mount only those from specific app(s)
    ]

Please **double check** if your ``url()`` call here has the path
argument **ending with a trailing slash** (e.g ``foo/bar/``). This is
required by the Django framework. You do not need to have this in your
``@url()`` decorator paths though.

Start serving apis
------------------

You can just start Django like normal, your apis will be automatically
discovered and mounted.

::

    ./manage.py runserver 0.0.0.0:8000

Note that for other developers to use your apis, you need to bind on
wildcard or public WAN/LAN accessable IP address specifically after
``runserver`` instead of leaving the param out to use the default
``127.0.0.1`` localhost IP. If you are developing inside a VM (e.g
through our *Vagrant* web dev vm) it is very important that you specify
the VM's IP or the wildcard IP after ``runserver`` so that you can use
your host machine's browser for accessing the apis through vm to host
forwarded ports.

Also, use ``runserver`` with ``DEBUG=true`` in ``settings.py`` will
automatically serve all the ``static/`` sub-folders (and those added by
``STATICFILES_DIRS``) from your apps. They are served like they were
merged under the same uri set by ``STATIC_URL`` in your ``settings.py``,
so if you do not want files from different apps to override each other,
put all your static assets (e.g \*.js/html/css/png) in a sub-folder with
the same name as your app inside each ``static/``. Though ``STATIC_URL``
doesn't have a default value, after running
``django-admin startproject`` your ``settings.py`` will set a default
value ``/static/`` to it so you could access files from the ``static/``
sub-folders under ``http://domain:8000/static/<file path>`` with zero
setup time.

If you are not using the ``runserver`` command for serving static assets
and service apis during development, make sure you call
``./manage.py collectstatics`` and serve folder ``STATIC_ROOT`` on
``STATIC_URL``, so that ``{% load static %}`` then
``{% static "images/hi.jpg" %}`` can work properly in your templates.

Adding RESTful services
-----------------------

Create apps in your Django project **normally**, this is to sub-divide
your services by app name for better maintainability. Optional though.

::

    ./manage.py startapp app_example
    ./manage.py startapp another_app_with_services

Function as service api
~~~~~~~~~~~~~~~~~~~~~~~

Add a ``services.py`` file in each app folder containing the service
functions ``fn(req, res, *args, **kwargs)`` decorated with ``@service``

::

    # proj/app_example/services.py
    from express.decorators import service, methods, url


    # /api/v1/absolute/url
    # /api/v1/app_example/relative/abcd

    @methods('GET', 'POST')
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

As you can see, you can still use regex captures in ``@url('..path..')``
if prefered. The captured group/named group will be passed normally to
your service function as positional args and keyword args. However,
**You can NOT use both positioned and namged group captures in the same
url!! Due to django implementation.**

Important Note
^^^^^^^^^^^^^^

Put ``@service`` as the inner-most decorator, other decorators don't
have this hard requirement on ordering here. You can still use all the
decorators from the Django web framework like ``@permission_required``
or ``@login_required`` but make sure they are all above ``@service``.

Argument APIs
^^^^^^^^^^^^^

The most important arguments to your service function would be the first
two, namely ``req`` for request and ``res`` for response. Here are the
available methods on these two objects.

req (ExpressRequest)
''''''''''''''''''''

-  req.params['key']
-  req.json
-  req.form
-  req.files['name']
-  req.cookies['name']
-  req['HTTP-HEADER']/req.header('key')

res (ExpressResponse)
'''''''''''''''''''''

-  res.redirect('url')
-  res.render(req, 'template', context={})
-  res.html('str')/text('str')
-  res.json(dict)
-  res.file('path')
-  res.attach('path')/download('path')
-  res.status(int)
-  res['HTTP\_HEADER']/res.header('key', val)

**Caveat:** ``res.status()`` and ``res['HTTP_HEADER']/res.header()``
must be called after
``.render()/html()/text()/json()/file()/attach()/download()`` in your
service function for new headers and status to be applied to the
response.

Model generated service apis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Within the ``models.py`` file, you can decorate any of your Model class
directly for it to generate the apis around its CRUD database
operations.

::

    # proj/app_example/models.py

    @url('/absolute/db/device')
    @url('db/device')
    @serve_unprotected
    class Device(models.Model):
        """docstring for Device"""
        sn = models.CharField(max_length=32)

This will mount 5 default service functions bound to different HTTP
methods (POST/GET/PUT,PATCH/DELETE/HEAD) to url
``app_example/models/Device`` for its CRUD database operations and one
more metadata operations.

Decorators
----------

For a function
~~~~~~~~~~~~~~

@service
^^^^^^^^

Turn your ``fn(req, res, *args, **kwargs)`` function into a Restful
service routine. Automatically detected if present in ``services.py`` in
any **installed** app.

-  Default path with ``services.urls``: ``/<app>/services/<fn>``
-  Default path wiht ``services.url(app)``: ``/services/<fn>``

You can change the mounting path by using the ``@url()`` decorator. You
can also use ``django.urls.reverse()`` to get the mount point by name
``<namespace>:<app>.<fn>``.

Still, **do not forget** to mount everthing collected inside
``services.urls`` to a root url in the django ``urls.py``. See the
**Setup** section above.

@methods(m1, m2, ...)
^^^^^^^^^^^^^^^^^^^^^

Allowed HTTP request methods to the service. You can also use ``@safe``
to allow only ``GET`` and ``HEAD`` requests.

@url(path)
^^^^^^^^^^

Override basic service auto-path (``/<app>/services/<fn>``). No need to
use ``r'..path..'`` here, what you put in ``path`` will be treated as
raw string automatically. Feel free to put regex group captures. **Just
don't mix named and annonymous capture groups in the url path, they
won't work together in django.**

You can use multiple ``@url()`` on the same service function.

@csrf
^^^^^

Setting CSRF token cookie on ``GET/HEAD`` requests to the service.
Checks and rejects ``POST/PUT/PATCH/DELETE`` requests according to their
csrf token + cookie pairs.

If you want an Ajax request to be guarded by django CSRF
(django.middleware.csrf.CsrfViewMiddleware) you need to ``GET/HEAD`` the
``@csrf`` decorated service first to have your CSRF cookie (named
``csrftoken``) set, then ``POST/PUT/PATCH/DELETE`` to it with real
requests including either ``X-CSRFToken`` in header or
``csrfmiddlewaretoken`` in a hidden form ``<input>`` field. The header
or hidden field value should match the value given by the cookie.

You can change the cookie and header names but **NOT** the hidden field
name in the django ``settings.py``.

For a Model
~~~~~~~~~~~

@serve
^^^^^^

Give a Model default RESTful apis to its CRUD operations. Default path
``/<app>/models/<Model>``

-  Default path with ``services.urls``: ``/<app>/models/<Model>``
-  Default path wiht ``services.url(app)``: ``/models/<Model>``

-  POST -- create -- {"payload": {...data...}}
-  GET -- read -- ?id= for single record, omit for all
-  PUT/PATCH -- update -- {"payload": {"id": "...", ...data...}}
-  DELETE -- delete -- ?id= for target record, required
-  HEAD -- meta -- model name ``X-Django-App-Model`` and table count
   ``X-DB-Table-Count`` in reply headers

When using **GET** http request for a model, you can also specify params
for filtering (by columns and Django ORM filter operations), sorting (by
columns) and paging the returned result.

::

    ?filter=foo1:op_and_val1&filter=foo2:op_and_val2
    ?sort=foo, -bar

    ?size=number
    ?offset=number
    ?page=number

Still, **do not forget** to mount everthing collected inside
``services.urls`` to a root url in the django ``urls.py``. See the
**Setup** section above.

@serve\_unprotected
^^^^^^^^^^^^^^^^^^^

Same as @serve but without csrf protection.

@url(path)
^^^^^^^^^^

Same as @url for a service function but with different default paths.

Licence
-------

Copyright 2017 Tim Lauv. Under the
`MIT <http://opensource.org/licenses/MIT>`__ License.

.. |PyPI-v| image:: https://img.shields.io/pypi/v/django-express.svg
   :target: https://pypi.python.org/pypi/django-express
.. |PyPI-pyv| image:: https://img.shields.io/pypi/pyversions/django-express.svg
   :target: https://pypi.python.org/pypi/django-express
.. |PypI-djangov| image:: https://img.shields.io/badge/Django-1.8%2C%201.9%2C%201.10-44B78B.svg
   :target: https://www.djangoproject.com/
