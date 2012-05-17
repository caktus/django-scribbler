"Models for storing snippet content."

import datetime

from django.contrib.auth.models import User
from django.db import models


class Snippet(model.Model):
    "Core model for storing snippet content."

    created_time = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, editable=False)
    modified_time = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(User, editable=False)
    name = models.CharField(max_length=255, blank=True, default=u"")
    slug = models.SlugField(max_length=255, blank=True, default=u"")
    url = models.CharField(max_length=255, blank=True, default=u"")
    content = models.TextField(blank=True, default=u"")
