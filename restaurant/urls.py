"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
# to call static files module
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from andalous import views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap



#### to active static when DEBUG = False ###
from django.views.static import serve
####################################"""" 


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('andalous.urls', namespace= 'blog')),
    url(r'^', include('cart.urls', namespace= 'cart')),
    url(r'^', include('orders.urls', namespace= 'orders')),
    url(r'^tinymce/', include('tinymce.urls')),
   

      # this to reset password via email
    path('', include('django.contrib.auth.urls')),

      #### to active static when DEBUG = False ###
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    ##########################################################################
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
