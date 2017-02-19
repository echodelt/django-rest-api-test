# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from . import views

router = routers.SimpleRouter(trailing_slash=True)

router.register(r'articles', views.ArticleViewSet, 'articles')

urlpatterns = [
    url(r'^', include(router.urls)),
]
