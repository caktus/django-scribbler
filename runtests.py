#!/usr/bin/env python
import sys
import os

import django
from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'scribbler',
        ),
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        SITE_ID=1,
        SECRET_KEY='super-secret',
        TEMPLATE_CONTEXT_PROCESSORS=(
            'django.contrib.auth.context_processors.auth',
            'django.core.context_processors.request',
        ),
        ROOT_URLCONF='scribbler.tests.urls',
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.jinja2.Jinja2',
                'DIRS': [os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates/jinja2')],
                'APP_DIRS': True,
                'OPTIONS': {'environment': 'scribbler.tests.jinja2.Environment',},
            },
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scribbler/tests')
                ],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                        'django.core.context_processors.debug',
                        'django.core.context_processors.media',
                        'django.core.context_processors.i18n',
                        'django.core.context_processors.static',
                        'django.core.context_processors.request',
                    ],
                    'debug': False,
                },
            },
        ],
        MIGRATION_MODULES={
            # these 'tests.migrations' modules don't actually exist, but this lets
            # us skip creating migrations for the test models.
            'scribbler': 'scribbler.tests.migrations',
            'dayslog': 'dayslog.tests.migrations',
        },
        MEDIA_ROOT = '',
        MEDIA_URL = '/media/',
        STATIC_ROOT = '',
        STATIC_URL = '/static/',
    )


from django.test.utils import get_runner


def runtests():
    if hasattr(django, 'setup'):
        django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['scribbler', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
