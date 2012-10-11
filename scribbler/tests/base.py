"Test helper functions and base test cases."
from __future__ import unicode_literals

import random
import string

from django.contrib.auth.models import User
from django.test import TestCase

from scribbler.models import Scribble


class ScribblerDataTestCase(TestCase):
    "Base test case for creating scribbler models."

    def get_random_string(self, length=10):
        return ''.join(random.choice(string.ascii_letters) for x in range(length))

    def create_scribble(self, **kwargs):
        "Factory method for creating Scribbles."
        defaults = {
            'name': self.get_random_string(),
            'slug': self.get_random_string(),
            'url': '/foo/',
        }
        defaults.update(kwargs)
        return Scribble.objects.create(**defaults)

    def create_user(self, **kwargs):
        "Factory method for creating Users."
        defaults = {
            'username': self.get_random_string(),
            'email': '',
            'password': self.get_random_string(),
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
