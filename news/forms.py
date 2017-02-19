# -*- coding: utf-8 -*-

import datetime

from django import forms
from datetimewidget.widgets import DateTimeWidget

dateTimeWidgetOptions = {
    'format': 'yyyy-mm-dd HH:ii',
    'autoclose': True,
    'showMeridian' : False
    }

class ArticleForm(forms.Form):

    title = forms.CharField(
        max_length=100,
        label="Title",
        required=True
        )
    description = forms.CharField(
        label="Description",
        required=True,
        widget=forms.Textarea
        )
    is_published = forms.BooleanField(
        initial=True,
        label = "Published",
        required=False
        )
    publication_date =  forms.DateTimeField(
        initial=datetime.datetime.now,
        label = "Publication date",
        required=True,
        widget=DateTimeWidget(
            options = dateTimeWidgetOptions,
            bootstrap_version=3
            )
        )
