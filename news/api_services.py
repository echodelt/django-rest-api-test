# -*- coding: utf-8 -*-

import logging
LOGGER = logging.getLogger(__name__)

import requests

from django.conf import settings
from django.urls import reverse
from django.utils.six import BytesIO

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .serializers import ArticleSerializer


DEFAULT_REQUESTS_HEADERS = {
    settings.API_AUTH_KEY_NAME: settings.API_AUTH_KEY_VALUE,
    "Accept": "application/json"
}

POST_PUT_REQUESTS_HEADERS = DEFAULT_REQUESTS_HEADERS.copy()
POST_PUT_REQUESTS_HEADERS.update({"Content-Type": "application/json"})


def decode_requests_response(content):
    stream = BytesIO(content)
    data = JSONParser().parse(stream)
    return data


class UnexpectedApiResponse(Exception):
    """
    Custom exception which may be raised by a client when he
    receives an unexpected response from the API service
    """

    def __init__(
        self,
        endpoint,
        method,
        payload,
        response_status_code,
        response_content,
        message=""
        ):
        super(UnexpectedApiResponse, self).__init__(message)
        self.endpoint = endpoint
        self.method = method
        self.payload = payload
        self.response_status_code = response_status_code
        self.response_content = response_content

    def __str__(self):
        return "Unexpected API response : " \
             + "endpoint : %s, " % self.endpoint \
             + "method : %s, " % self.method \
             + "payload : %s, " % self.payload \
             + "response code : %s, " % self.response_status_code \
             + "response content : %s" % self.response_content


def get_articles():
    """
    Retreives the articles list (via an API request)
    """

    endpoint = "%s%s" % (
        settings.API_BASE_URL,
        reverse("api:articles-list")
        )
    headers = DEFAULT_REQUESTS_HEADERS
    r = requests.get(
        endpoint,
        headers=DEFAULT_REQUESTS_HEADERS
        )

    if r.status_code != 200:
        raise UnexpectedApiResponse(
            endpoint=endpoint,
            method="GET",
            payload=None,
            response_status_code=r.status_code,
            response_content=r.content
            )

    raw_data = decode_requests_response(r.content)
    serializer = ArticleSerializer(data=raw_data, many=True)
    serializer.is_valid(raise_exception=True)
    articles = serializer.validated_data
    return articles


def get_article(pk):
    """
    Retreives an article identified by its primary key (via an API request)
    """

    endpoint = "%s%s" % (
        settings.API_BASE_URL,
            reverse("api:articles-detail", kwargs={'pk': pk})
            )
    headers = DEFAULT_REQUESTS_HEADERS
    r = requests.get(
        endpoint,
        headers=headers
        )

    if r.status_code != 200:
        raise UnexpectedApiResponse(
            endpoint=endpoint,
            method="GET",
            payload=None,
            response_status_code=r.status_code,
            response_content=r.content
            )

    raw_data = decode_requests_response(r.content)
    serializer = ArticleSerializer(data=raw_data)
    serializer.is_valid(raise_exception=True)
    article = serializer.validated_data
    return article


def create_article(article):
    """
    Creates an article (via an API request)
    """

    serializer = ArticleSerializer(data=article)
    serializer.is_valid(raise_exception=True)

    endpoint = "%s%s" % (
        settings.API_BASE_URL, reverse("api:articles-list")
        )
    headers = POST_PUT_REQUESTS_HEADERS
    payload = JSONRenderer().render(serializer.validated_data)
    r = requests.post(
        endpoint,
        headers=headers,
        data=payload
        )

    if r.status_code != 201:
        raise UnexpectedApiResponse(
            endpoint=endpoint,
            method="POST",
            payload=payload,
            response_status_code=r.status_code,
            response_content=r.content
            )

    response_data = decode_requests_response(r.content)
    serializer = ArticleSerializer(data=response_data)
    serializer.is_valid(raise_exception=True)
    article = serializer.validated_data
    return article["id"]


def update_article(pk, article):
    """
    Creates an article (via an API request)
    """

    serializer = ArticleSerializer(data=article)
    serializer.is_valid(raise_exception=True)
    endpoint = "%s%s" % (
        settings.API_BASE_URL, reverse("api:articles-detail", kwargs={'pk': pk})
        )
    headers = POST_PUT_REQUESTS_HEADERS
    payload = JSONRenderer().render(serializer.validated_data)
    r = requests.put(
        endpoint,
        headers=headers,
        data=payload
        )

    if r.status_code != 200:
        raise UnexpectedApiResponse(
            endpoint=endpoint,
            method="PUT",
            payload=payload,
            response_status_code=r.status_code,
            response_content=r.content
            )

    return True


def delete_article(pk):
    """
    Deletes an article (via an API request)
    """

    endpoint = "%s%s" % (
        settings.API_BASE_URL, reverse("api:articles-detail", kwargs={'pk': pk})
        )
    headers = DEFAULT_REQUESTS_HEADERS
    r = requests.delete(
        endpoint,
        headers=headers
        )

    if r.status_code != 204:
        raise UnexpectedApiResponse(
            endpoint=endpoint,
            method="DELETE",
            payload=None,
            response_status_code=r.status_code,
            response_content=r.content
            )

    return True
