# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publication_date',
            field=models.DateTimeField(verbose_name='publication date'),
        ),
    ]
