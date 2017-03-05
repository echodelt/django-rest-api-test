# -*- coding: utf-8 -*-

import json
import datetime, pytz
import sys

from django.test import LiveServerTestCase
from django.test.utils import override_settings

from rest_framework import serializers

import api
from . import api_services


FIXTURES = ["test_data"]


class ApiServicesTest(LiveServerTestCase):
    fixtures = FIXTURES

    def test_get_articles(self):
        #with override_settings(API_BASE_URL=ApiServicesTest.live_server_url):
        # with self.settings(API_BASE_URL=self.live_server_url):
        with override_settings(API_BASE_URL=self.live_server_url):
            articles = api_services.get_articles()
            self.assertEqual(len(articles), 2)


    def test_get_article_with_wrong_pk(self):
        with override_settings(API_BASE_URL=self.live_server_url):
            article_pk = 999
            with self.assertRaises(api_services.UnexpectedApiResponse) as except_context:
                article = api_services.get_article(pk=article_pk)
            self.assertEqual(except_context.exception.response_status_code, 404)


    def test_get_article_with_right_pk(self):
        with override_settings(API_BASE_URL=self.live_server_url):
            article_pk = 1
            article = api_services.get_article(pk=article_pk)
            self.assertEqual(article["title"], "1st article")
            self.assertEqual(article["description"], "1st article content")
            self.assertEqual(article["is_published"], False)
            self.assertEqual(article["publication_date"], datetime.datetime(
                year=2017,
                month=2,
                day=16,
                hour=12,
                minute=12,
                second=49,
                tzinfo=pytz.utc
                )
            )


    def test_create_article_with_invalid_data(self):
        with override_settings(API_BASE_URL=self.live_server_url):
            articles_num_before = api.models.Article.objects.all().count()

            article_title = "3rd article"

            article = {
                 "title": article_title,
                 }

            with self.assertRaises(Exception) as except_context:
                article = api_services.create_article(article=article)


    def test_create_article_with_valid_data(self):
        with override_settings(API_BASE_URL=self.live_server_url):
            articles_num_before = api.models.Article.objects.all().count()

            article_title = "3rd article"
            article_description = "3rd article content"
            article_is_published = True
            article_publication_date = datetime.datetime(
               year=2017,
               month=3,
               day=1,
               hour=12,
               minute=17,
               second=0,
               tzinfo=pytz.utc
               )

            article = {
                 "title": article_title,
                 "description": article_description,
                 "is_published": article_is_published,
                 "publication_date": article_publication_date
                 }

            article_id = api_services.create_article(article)

            articles_num_after = api.models.Article.objects.all().count()
            self.assertEqual(articles_num_after, articles_num_before + 1)

            saved_article = api.models.Article.objects.get(pk=article_id)
            self.assertEqual(saved_article.title, article_title)
            self.assertEqual(saved_article.description, article_description)
            self.assertEqual(saved_article.is_published, article_is_published)
            self.assertEqual(saved_article.publication_date, article_publication_date)


    def test_update_article_with_wrong_pk(self):
        with override_settings(API_BASE_URL=self.live_server_url):
            article_pk = 999

            updated_article_title = "1st article (new)"
            updated_article_description = "1st article content (new)"
            updated_article_is_published = False
            updated_article_publication_date = datetime.datetime(
               year=2017,
               month=3,
               day=1,
               hour=12,
               minute=17,
               second=0,
               tzinfo=pytz.utc
               )

            updated_article = {
                 "title": updated_article_title,
                 "description": updated_article_description,
                 "is_published": updated_article_is_published,
                 "publication_date": updated_article_publication_date
                 }

            with self.assertRaises(api_services.UnexpectedApiResponse) as except_context:
                article = api_services.get_article(pk=article_pk)
            self.assertEqual(except_context.exception.response_status_code, 404)


    def test_update_article_with_right_pk_invalid_data(self):
        with override_settings(API_BASE_URL=self.live_server_url):
            article_pk = 1

            updated_article_title = "1st article (new)"

            updated_article = {
                 "title": updated_article_title,
                 }

            with self.assertRaises(Exception) as except_context:
                api_services.update_article(article_pk, updated_article)


    def test_update_article_with_right_pk_right_data(self):
        with override_settings(API_BASE_URL=self.live_server_url):
            article_pk = 1

            updated_article_title = "1st article (new)"
            updated_article_description = "1st article content (new)"
            updated_article_is_published = False
            updated_article_publication_date = datetime.datetime(
               year=2017,
               month=3,
               day=1,
               hour=12,
               minute=17,
               second=0,
               tzinfo=pytz.utc
               )

            updated_article = {
                 "title": updated_article_title,
                 "description": updated_article_description,
                 "is_published": updated_article_is_published,
                 "publication_date": updated_article_publication_date
                 }

            article_id = api_services.update_article(article_pk, updated_article)

            saved_article = api.models.Article.objects.get(pk=article_pk)
            self.assertEqual(saved_article.title, updated_article_title)
            self.assertEqual(saved_article.description, updated_article_description)
            self.assertEqual(saved_article.is_published, updated_article_is_published)
            self.assertEqual(saved_article.publication_date, updated_article_publication_date)


    def test_delete_article_with_wrong_pk(self):
        with override_settings(API_BASE_URL=self.live_server_url):
            article_pk = 999
            with self.assertRaises(api_services.UnexpectedApiResponse) as except_context:
                article = api_services.delete_article(pk=article_pk)
            self.assertEqual(except_context.exception.response_status_code, 404)


    def test_delete_article_with_right_pk(self):
        with override_settings(API_BASE_URL=self.live_server_url):
            articles_num_before = api.models.Article.objects.all().count()

            article_pk = 1

            res =  api_services.delete_article(pk=article_pk)
            self.assertEqual(res, True)

            articles_num_after = api.models.Article.objects.all().count()
            self.assertEqual(articles_num_after, articles_num_before - 1)

            with self.assertRaises(api.models.Article.DoesNotExist):
                api.models.Article.objects.get(pk=article_pk)
