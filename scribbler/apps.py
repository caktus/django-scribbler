# -*- coding: utf-8 -*-
from django.apps import AppConfig


class ScribblerAppConfig(AppConfig):
    name = 'scribbler'
    verbose_name = "Scribbler"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from django.conf import settings
        from django.core.exceptions import ImproperlyConfigured
        TEMPLATES = getattr(settings, 'TEMPLATES', None)
        if TEMPLATES is None:
            django_templates_used = True
        else:
            django_templates_used = False
            for config in TEMPLATES:
                if config.get('BACKEND', '') == 'django.template.backends.django.DjangoTemplates':
                    django_templates_used = True
                    break
        if not django_templates_used:
            raise ImproperlyConfigured("Django-scribbler requires 'django.template.backends.django.DjangoTemplates' to be used as templates engine")
