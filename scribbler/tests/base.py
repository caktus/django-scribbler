"Test helper functions and base test cases."

import random
import string

from django.test import TestCase

from scribbler.models import Scribble


class ScribblerDataTestCase(TestCase):
    "Base test case for creating scribbler models."

    def get_random_string(self, length=10):
        return u''.join(random.choice(string.ascii_letters) for x in xrange(length))

    def create_scribble(self, **kwargs):
        "Factory method for creating Scribbles."
        defaults = {
            'name': self.get_random_string(),
            'slug': self.get_random_string(),
            'url': '/foo/',
        }
        defaults.update(kwargs)
        return Scribble.objects.create(**defaults)
