# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('decription', models.TextField(verbose_name='decription')),
                ('is_published', models.BooleanField(default=False, verbose_name='is published')),
                ('publication_date', models.DateTimeField(auto_now_add=True, verbose_name='publication date')),
            ],
            options={
                'verbose_name_plural': 'articles',
            },
        ),
    ]
