Getting Started
====================================

Below are the basic steps need to get django-scribbler integrated into your
Django project.

Install Scribbler
------------------------------------

django-scribbler should be installed using ``pip``::

    $ pip install django-scribbler

.. note:: If you need to run an unreleased version from the repository, see :doc:`contributing` for additional instructions.

Configure Settings
------------------------------------

You need to include ``scribbler`` to your installed apps. django-scribbler requires
``django.contrib.auth`` which in turn requires ``django.contrib.sessions``
which are enabled in Django by default. You will also need to include a context processor
to include the current request in the template context. This is included by default
in Django 1.8+ when using the ``startproject`` command.

.. code-block:: python

    INSTALLED_APPS = (
        # Required contrib apps
        'django.contrib.auth',
        'django.contrib.sessions',
        # Other installed apps would go here
        'scribbler',
    )

    ...

    TEMPLATES = [ # example config untill 'context_processors' your config maydiffer
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    # add required context processors here:
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    # Other context processors would go here
                ],
                'debug': False,
            },
        },
    ],


Django 1.8+ also supports custom template engines
but this is not supported at the moment by django-scribbler.

For the context processor to have any effect you need to make sure that the template
is rendered using a RequestContext. This is done for you with the
`render <https://docs.djangoproject.com/en/stable/topics/http/shortcuts/#render>`_ shortcut.

django-scribbler aggressively caches the scribble content. By default the scribble
content is cached for 12 hours. You have the option to configure this cache timeout
with the ``SCRIBBLER_CACHE_TIMEOUT`` setting. The value should be the timeout in
seconds.


Configure Urls
------------------------------------

You should include the scribbler urls in your root url patterns.

.. code-block:: python

    urlpatterns = [
        # Other url patterns would go here
        url(r'^scribbler/', include('scribbler.urls')),
    ]


Create Database Tables
------------------------------------

You'll need to create the necessary database tables for storing scribble content.
To run migrations call::

    python manage.py migrate scribbler


User Permissions
------------------------------------

To edit scribbles on the front-end users must have the ``scribbler.add_scribble``
and ``scribbler.change_scribble`` permissions. You can configure uses to have
these permissions through the users section of the Django admin. Superusers have
all of these permissions by default.

Similarly, to edit fields from models on the front-end, users must have "change"
permission for the models being edited. Again these permissions can be configured
through the users section of the Django admin.


Include Static Resources
------------------------------------

django-scribbler includes both CSS and JS resources which need to be included in your
templates to handle the front-end content management. Since you may want to include
scribbles on any page on your site these should be included in your base template ``<head>``.

.. code-block:: html

    <link rel="stylesheet" href="{% static 'scribbler/css/scribbler.css' %}">
    <script src="{% static 'scribbler/js/scribbler-min.js' %}"></script>

This uses `Browserify <http://browserify.org/>`_ to load the additional JS resources. The front-end
editor uses `CodeMirror <http://codemirror.net/>`_ (currently using v5.10) which is included in the distribution.
Both Browserify and CodeMirror are available a MIT-style license compatible with
this project's BSD license. You can find the license files included in
``scribbler/static/scribbler/libs/``.


Place Scribbles in Your Template
------------------------------------

You are now ready to place the scribble content blocks throughout your templates.
This is done with the ``scribble`` block tag. The basic usage of the tag takes
one argument which is the slug name for the scribble. Slugs must be unique per
url/slug pair. That means you cannot use the same slug more than once in the
template but you can use the same slug in different templates as long as they
are rendered on different urls.

.. code-block:: html

    {% load scribbler_tags %}
    {% scribble 'header' %}
        <p>Blip {% now 'Y' %} {{ STATIC_URL|upper }}</p>
    {% endscribble %}

The content inside the block is the default content that will be rendered if a
matching scribble in the database is not found.

The ``scribble`` tag can take an optional argument which allows for defining
shared scribbles.

.. code-block:: html

    {% load scribbler_tags %}
    {% scribble 'header' 'shared' %}
        <p>Blip {% now 'Y' %} {{ STATIC_URL|upper }}</p>
    {% endscribble %}

The second argument defines a lookup vector to a shared scribble. This overrides
the url portion of the url/slug pair, and allows for reuse across multiple templates.

.. note::

    Scribble content can be any valid Django template. However the content does
    not include all of the context of the template. Only the context provided
    by the set of ``context_processors`` from the ``TEMPLATES`` configuration.


A second scribbler tag, ``scribble_field``, allows for editing fields of model instances.
For example, suppose you have a ``DaysLog`` model with a field named ``happenings``. Suppose
an instance of this model is passed into your template in the template variable ``days_log``.
Then the ``happenings`` field of this ``DaysLog`` instance can be displayed and edited on the
page by including this ``scribble_field`` template tag in the template for the page:

.. code-block:: html

    {% load scribbler_tags %}
    {% scribble_field days_log 'happenings' %}

.. note::

    The logged-in user must have "change" permission for the model in order for
    the model instance to be editable on the page.

That should be enough to get you up and running with django-scribbler.
