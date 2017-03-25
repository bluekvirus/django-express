"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from express import services

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Need to use include() here as urls.py is consulted before apps ready.
    # There is no service auto-discovery before that point, thus no services.urls. 
    url(r'^api/v1/', include(services.urls, namespace='express')),
    url(r'^testb/api/v1/', include(services.url('testb', noprefix=True), namespace='testb')),
]
