# -*- coding: utf-8 -*-

import logging
LOGGER = logging.getLogger(__name__)

import functools

from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.http import Http404

from .forms import ArticleForm

from django.views.generic.edit import FormView

from . import api_services


def processExceptions(func):
    """
    Intercepts and logs exceptions which may be raised
    during view processing
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except api_services.UnexpectedApiResponse as e:
            LOGGER.exception(e)
            if e.response_status_code == 404:
                raise Http404
            raise
        except Exception as e:
            LOGGER.exception(e)
            raise
    return wrapper


class ArticlesList(View):
    @processExceptions
    def get(self, request):
        articles = api_services.get_articles()
        context = {
            "page_title": "Dashboard",
            "articles": articles
            }
        return render(request, 'news/articles_list.html', context)


class ArticleDetail(View):
    @processExceptions
    def get(self, request, pk):
        article = api_services.get_article(pk)
        context = {
            "page_title": "Detail : %s" % article["title"],
            "article": article
            }
        return render(request, 'news/article_detail.html', context)


class ArticleCreate(FormView):

    template_name = 'news/article_create.html'
    form_class = ArticleForm

    @processExceptions
    def form_valid(self, form):
        article = data=form.cleaned_data
        id = api_services.create_article(article)
        return redirect("news:article_detail", pk=id)

    def get_context_data(self, **kwargs):
        context = super(ArticleCreate, self).get_context_data(**kwargs)
        context['page_title'] = "Article creation"
        return context


class ArticleUpdate(FormView):

    template_name = 'news/article_update.html'
    form_class = ArticleForm

    @processExceptions
    def get_initial(self):
        initial = super(ArticleUpdate, self).get_initial()
        self.article = api_services.get_article(self.kwargs['pk'])
        initial.update(self.article)
        return initial

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data(**kwargs)
        context['page_title'] = "Article update : %s" % self.article["title"]
        context['article'] = self.article
        return context

    @processExceptions
    def form_valid(self, form):
        article = data=form.cleaned_data
        id = api_services.update_article(self.kwargs['pk'], article)
        return redirect("news:article_detail", pk=self.kwargs['pk'])


class ArticleDelete(View):
    @processExceptions
    def get(self, request, pk):
        article = api_services.get_article(pk)
        context = {
            "page_title": "Article deletion : %s" % article["title"],
            "article": article
            }
        return render(request, 'news/article_delete.html', context)

    @processExceptions
    def post(self, request, pk):
        api_services.delete_article(pk)
        return redirect("news:articles_list")
