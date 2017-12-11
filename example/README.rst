Example Project
===============

This is a very simple example project to demonstrate the use of django-scribbler.

Setup instructions:

1. Create a virtualenv and install requirements::

     mkvirtualenv -p $(which python3) scribbler
     pip install -r requirements.txt

#. Setup the SQLite database and a superuser (set password to "demo")::

     python manage.py migrate
     python manage.py createsuperuser --username demo

#. Run the server::

     python manage.py runserver
