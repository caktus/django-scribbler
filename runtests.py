#!/usr/bin/env python
import sys

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
        SITE_ID=1,
        SECRET_KEY='super-secret',
        TEMPLATE_CONTEXT_PROCESSORS=(
            'django.core.context_processors.request',
        ),
        ROOT_URLCONF='scribbler.tests.urls',
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
    )


from django.test.utils import get_runner


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['scribbler', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()

