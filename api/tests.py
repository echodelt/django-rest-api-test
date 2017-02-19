# -*- coding: utf-8 -*-

import json
import datetime

from django.conf import settings
from django.test import TestCase

from .models import Article


FIXTURES = ["test_data"]

HTTP_API_AUTH_KEY_NAME = "HTTP_%s" % settings.API_AUTH_KEY_NAME.upper()
API_AUTH_KEY_VALUE = settings.API_AUTH_KEY_VALUE


class ApiTest(TestCase):
    fixtures = FIXTURES

    def test_get_articles_without_auth_key(self):
        headers = {
            "HTTP_ACCEPT": "application/json"
        }
        response = self.client.get(
            "/api/articles/",
            **headers
            )
        self.assertEqual(response.status_code, 403)


    def test_get_articles_with_wrong_auth_key(self):
        headers = {
            HTTP_API_AUTH_KEY_NAME: "aaaaaaaaa",
            "HTTP_ACCEPT": "application/json"
            }
        response = self.client.get(
            "/api/articles/",
            **headers
            )
        self.assertEqual(response.status_code, 403)


    def test_get_articles_with_right_auth_key_wrong_accept(self):
        headers = {
            HTTP_API_AUTH_KEY_NAME: API_AUTH_KEY_VALUE,
            "HTTP_ACCEPT": "application/xml"
            }
        response = self.client.get(
            "/api/articles/",
            **headers
            )
        self.assertEqual(response.status_code, 406)


    def test_get_articles_with_right_auth_key_right_accept(self):
        headers = {
            HTTP_API_AUTH_KEY_NAME: API_AUTH_KEY_VALUE,
            "HTTP_ACCEPT": "application/json"
            }

        response = self.client.get(
            "/api/articles/",
            **headers
            )

        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        self.assertEqual(len(json_resp), 2)


    def test_get_article_with_right_auth_key_right_accept(self):
        headers = {
            HTTP_API_AUTH_KEY_NAME: API_AUTH_KEY_VALUE,
            "HTTP_ACCEPT": "application/json"
            }

        response = self.client.get(
            "/api/articles/1/",
            **headers
            )

        self.assertEqual(response.status_code, 200)

        json_resp = response.json()
        self.assertEqual(json_resp["title"], "1st article")


    def test_create_article_with_right_auth_key(self):
        articles_num_before = Article.objects.all().count()

        headers = {
            HTTP_API_AUTH_KEY_NAME: API_AUTH_KEY_VALUE,
            "HTTP_ACCEPT": "application/json"
            }

        payload = {
            "title": "3rd article",
            "description": "3rd article content",
            "is_published": True,
            "publication_date": datetime.datetime.now().isoformat()
            }

        response = self.client.post(
            "/api/articles/",
            data=json.dumps(payload),
            content_type="application/json",
            **headers
            )

        self.assertEqual(response.status_code, 201)

        articles_num_after = Article.objects.all().count()
        self.assertEqual(articles_num_after, articles_num_before + 1)

        json_resp = response.json()
        article_id = json_resp["id"]
        article = Article.objects.get(id=article_id)
        self.assertEqual(article.title, "3rd article")
