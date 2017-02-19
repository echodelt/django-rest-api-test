django-rest-api-test
==================

A simple Django test project (news management system) exposing and consuming
locally a REST API implemented with the help of the Django Rest Framework.

This project uses SQLite as the backend database. Its setup requires only the
following steps :

    mkvirtualenv django-rest-api-test -p /usr/bin/python3.4

    pip install -r requirements.txt

    python manage.py migrate

    python manage.py runserver

And you can then navigate to localhost:8000.

Tested with Django 1.10 and Python 3.4 / 3.5.
