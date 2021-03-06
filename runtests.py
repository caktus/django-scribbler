#!/usr/bin/env python
import sys
import os
from optparse import OptionParser

import django
from django.conf import settings
from django.test.utils import get_runner

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
            'django.contrib.staticfiles',
            'scribbler',
        ),
        MIDDLEWARE=(
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),
        SECRET_KEY='super-secret',

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
                        'django.template.context_processors.debug',
                        'django.template.context_processors.media',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.static',
                        'django.template.context_processors.request',
                    ],
                    'debug': False,
                },
            },
        ],
        MIGRATION_MODULES={
            # this lets us skip creating migrations for the test models.
            # https://docs.djangoproject.com/en/2.2/ref/settings/#migration-modules
            'scribbler': None,
            'dayslog': None,
        },
        MEDIA_ROOT='',
        MEDIA_URL='/media/',
        STATIC_ROOT='',
        STATIC_URL='/static/',
        LOGIN_REDIRECT_URL='/test/'
    )


def runtests(*test_args, **kwargs):
    django.setup()
    if not test_args:
        test_args = ['scribbler', ]
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    parser = OptionParser()

    (options, args) = parser.parse_args()
    runtests(*args)
