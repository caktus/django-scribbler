"Models for storing snippet content."
from __future__ import unicode_literals

from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
try:
    from django.utils.six import PY3
except ImportError:
    # Django < 1.5. No Python 3 support
    PY3 = False


from .conf import CACHE_TIMEOUT, CACHE_KEY_FUNCTION


class Scribble(models.Model):
    "Core model for storing snippet content."

    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    modified_time = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=255, blank=True, default="")
    slug = models.SlugField(max_length=255, blank=True, default="")
    url = models.CharField(max_length=255, blank=True, default="")
    content = models.TextField(blank=True, default="")

    def __str__(self):
        return '{0} - {1}'.format(self.slug, self.url)

    if not PY3:
        __unicode__ = __str__
        __str__ = lambda self: self.__unicode__().encode('utf-8')

    class Meta(object):
        unique_together = ('slug', 'url')

    @models.permalink
    def get_save_url(self):
        if self.pk:
            return ('edit-scribble', (), {'scribble_id': self.pk})
        else:
            return ('create-scribble', (), {})

    @models.permalink
    def get_delete_url(self):
        return ('delete-scribble', (), {'scribble_id': self.pk})


@receiver(post_save, sender=Scribble)
def update_scribble_cache(sender, instance, **kwargs):
    "Update scribble cache on save."
    if CACHE_TIMEOUT:
        key = CACHE_KEY_FUNCTION(slug=instance.slug, url=instance.url)
        cache.set(key, instance, CACHE_TIMEOUT)


@receiver(post_delete, sender=Scribble)
def populate_scribble_cache(sender, instance, **kwargs):
    "Populate cache with empty scribble cache on delete."
    if CACHE_TIMEOUT:
        key = CACHE_KEY_FUNCTION(slug=instance.slug, url=instance.url)
        scribble = Scribble(slug=instance.slug, url=instance.url)
        cache.set(key, scribble, CACHE_TIMEOUT)


@receiver(pre_save, sender=Scribble)
def clear_scribble_cache(sender, instance, **kwargs):
    "Clear cache pre-save in case slug/url has changed."
    if CACHE_TIMEOUT:
        raw = kwargs.get('raw', False)
        if instance.pk and not raw:
            # Need original slug/url from the DB
            original = Scribble.objects.get(pk=instance.pk)
            key = CACHE_KEY_FUNCTION(slug=original.slug, url=original.url)
            cache.delete(key)
