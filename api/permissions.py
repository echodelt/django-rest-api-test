# -*- coding: utf-8 -*-

from django.conf import settings
from rest_framework import permissions

class ApiAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.META.get("HTTP_%s" % settings.API_AUTH_KEY_NAME.upper()) == settings.API_AUTH_KEY_VALUE
