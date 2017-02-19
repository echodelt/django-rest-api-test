# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

app_name = 'news'

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='news:articles_list')),
    url(r'^articles/$', views.ArticlesList.as_view(), name='articles_list'),
    url(r'^articles/(?P<pk>\d+)/$', views.ArticleDetail.as_view(), name='article_detail'),
    url(r'^articles/create/$', views.ArticleCreate.as_view(), name='article_create'),
    url(r'^articles/(?P<pk>\d+)/update/$', views.ArticleUpdate.as_view(), name='article_update'),
    url(r'^articles/(?P<pk>\d+)/delete/$', views.ArticleDelete.as_view(), name='article_delete'),
    ]
