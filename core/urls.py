# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf.urls import handler404, handler500
from .views import custom_handler404, custom_handler500

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='news:articles_list')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^admin/', admin.site.urls),
    url(r'^errors/404/$', custom_handler404, name='error-404'),
    url(r'^errors/500/$', custom_handler500, name='error-500'),
]

handler404 = custom_handler404
handler500 = custom_handler500
