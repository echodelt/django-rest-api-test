# -*- coding: utf-8 -*-

from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', required=False)
    title = serializers.CharField(label='Title', max_length=100)
    description = serializers.CharField(label='Description')
    is_published = serializers.BooleanField(label='Is published', required=False)
    publication_date = serializers.DateTimeField(label='Publication date')
