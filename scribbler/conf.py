"Default settings for django-scribbler."

import hashlib

from django.conf import settings


DEFAULT_TIMEOUT = 12 * 60 * 60

CACHE_TIMEOUT = getattr(settings, 'SCRIBBLER_CACHE_TIMEOUT', DEFAULT_TIMEOUT)

CACHE_PREFIX = u'scribbler'


def default_cache_key(slug, url):
    "Construct a cache key for a given slug/url pair."
    sha = hashlib.sha1(b'{0}#{1}'.format(url, slug))
    return u'{0}:{1}'.format(CACHE_PREFIX, sha.hexdigest())


CACHE_KEY_FUNCTION = default_cache_key # Not currently configurable
