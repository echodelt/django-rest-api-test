# -*- coding: utf-8 -*-

from django.db import models

class Article(models.Model):
    class Meta:
        verbose_name_plural = 'articles'

    title = models.CharField(
        max_length=100,
        verbose_name="title"
        )
    description = models.TextField(
        verbose_name="decription"
        )
    is_published = models.BooleanField(
        default=False,
        verbose_name = "is published"
        )
    publication_date =  models.DateTimeField(
        verbose_name = "publication date"
        )

    def __str__(self):
        return self.title
