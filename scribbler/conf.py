"Default settings for django-scribbler."
from __future__ import unicode_literals

import hashlib

from django.conf import settings


DEFAULT_TIMEOUT = 12 * 60 * 60

CACHE_TIMEOUT = getattr(settings, 'SCRIBBLER_CACHE_TIMEOUT', DEFAULT_TIMEOUT)

CACHE_PREFIX = 'scribbler'


def default_cache_key(slug, url):
    "Construct a cache key for a given slug/url pair."
    sha = hashlib.sha1('{0}#{1}'.format(url, slug).encode('ascii'))
    return '{0}:{1}'.format(CACHE_PREFIX, sha.hexdigest())


CACHE_KEY_FUNCTION = default_cache_key # Not currently configurable
