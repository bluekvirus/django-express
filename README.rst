django-express
==============

Easy Restful APIs with the Django web framework. (Python 3.3+, Django
1.7+)

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
        url(r'^api/v1/', include(services.urls)) # e.g mount them on /api/v1/<app>/<fn>
    ]

Add RESTful services
--------------------

Create apps in your Django project normally

::

    ./manage.py startapp app_example

Then add a ``services.py`` file in an app folder containing all the
service functions

::

    # proj/app_example/services.py

    from express.decorators import service, methods, url

    # /api/v1/absolute/url

    @url('/absolute/url')
    @methods(['GET', 'POST'])
    @service
    def abc(req, res, *args, **kwargs):
        res.json({**req.GET, **req.POST})

    # /api/v1/app_example/efg

    @service
    def efg(req, res, *args, **kwargs):
        res.html('Nothing but a test from <h2>{}</h2>'.format(__name__))

    # /api/v1/app_example/hij

    @service
    def hij(req, res, *args, **kwargs):
        res.file('db.sqlite3')

    # /api/v1/app_example/x

    @service
    def x(req, res, *args, **kwargs):
        res.text('Nothing but a test from {}'.format(__name__))

    # /api/v1/app_example/relative/url/y-service

    @url('relative/url/y-service')
    @service
    def y(req, res, *args, **kwargs):
        res.json({
            'data': 'Nothing but a test from {}'.format(__name__),
            'text': 123
        })
        res.header('Hello~', 'World!') # header
        res.status(201) # status

    # /api/v1/app_example/z

    @service
    def z(req, res, *args, **kwargs):
        res.download('db.sqlite3')

Important Note
--------------

Put ``@service`` as the inner-most decorator, other decorators don't
have this hard requirement on ordering here. You can still use all the
decorators from the Django web framework like ``@permission_required``
or ``@login_required`` but make sure they are all above ``@service``.

APIs
----

req (ExpressRequest)
~~~~~~~~~~~~~~~~~~~~

-  req.params['key']
-  req.json
-  req.form
-  req.files['name']
-  req.cookies['name']
-  req['HTTP-HEADERs']

res (ExpressResponse)
~~~~~~~~~~~~~~~~~~~~~

-  res.html()/text()
-  res.json()
-  res.file()
-  res.attach()/download()
-  res.status()
-  res.header()
-  res.redirect()

Decorators
----------

@service
~~~~~~~~

@methods
~~~~~~~~

@url
~~~~

@csrf
~~~~~

Licence
-------

Copyright 2017 Tim Lauv. Under the
`MIT <http://opensource.org/licenses/MIT>`__ License.
