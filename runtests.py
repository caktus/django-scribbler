#!/usr/bin/env python
import sys

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

