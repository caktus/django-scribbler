# -*- coding: utf-8 -*-

"Test for template tags."
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.template import Template, TemplateSyntaxError
from django.template.context import RequestContext
from django.test.client import RequestFactory
from unittest import skipIf

from . import DaysLog
from .base import ScribblerDataTestCase
from scribbler.conf import CACHE_TIMEOUT

class UnicodeURLTestCase(ScribblerDataTestCase):
    "Test, that unicode characters in url got cached"

    def testUnicodeURL(self):
        scribble = self.create_scribble(
            url='/foo/čřžžýü', slug='sidebar',
            content='<p>Scribble content.</p>'
        )
        self.assertEquals(scribble.url, "/foo/čřžžýü")


class RenderScribbleTestCase(ScribblerDataTestCase):
    "Tag to render a scribble for the current page."

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/foo/')
        self.scribble = self.create_scribble(
            url='/foo/', slug='sidebar',
            content='<p>Scribble content.</p>'
        )

    def tearDown(self):
        # Transaction will be rolled back without calling delete
        # so we need to clear the cache between runs
        cache.clear()

    def render_template_tag(self, slug, context=None, default='<p>Default.</p>', url=None):
        "Render the template tag."
        context = context or {}
        if not url:
            tag = '{{% load scribbler_tags %}}{{% scribble {0} %}}{1}{{% endscribble %}}'
        else:
            tag = '{{% load scribbler_tags %}}{{% scribble {0} {2} %}}{1}{{% endscribble %}}'
        template = Template(tag.format(slug, default, url))
        context = RequestContext(self.request, context)
        return template.render(context)

    def test_basic_rendering(self):
        "Render a scribble by the slug."
        result = self.render_template_tag(slug='"sidebar"')
        self.assertTrue('<p>Scribble content.</p>' in result)

    def test_variable_slug(self):
        "Render a scribble by the slug as a context variable."
        result = self.render_template_tag(slug='foo', context={'foo': 'sidebar'})
        self.assertTrue('<p>Scribble content.</p>' in result, result)

    def test_slug_not_found(self):
        "Render default if scribble not found by slug."
        self.scribble.slug = 'blip'
        self.scribble.save()
        result = self.render_template_tag(slug='"sidebar"')
        self.assertTrue('<p>Default.</p>' in result)

    def test_url_not_found(self):
        "Render default if scribble not found for the current url."
        self.scribble.slug = '/bar/'
        self.scribble.save()
        result = self.render_template_tag(slug='"sidebar"')
        self.assertTrue('<p>Default.</p>' in result)

    def test_default_rendering(self):
        "Render default if no scribbles exist."
        self.scribble.delete()
        result = self.render_template_tag(slug='"sidebar"')
        self.assertTrue('<p>Default.</p>' in result)

    def test_unicode_rendering(self):
        "Render with unicode defaults when no scribbles exist."
        # On Django>=1.9 ScribbleFormMixin.clean_content directly uses django.template.Template
        # and also uses force_text that may fail for non-string objects that have __str__ with
        # unicode output.
        self.scribble.delete()
        unicode_default = '<p>\u0422\u0435\u043a\u0441\u0442.</p>'
        result = self.render_template_tag(slug='"sidebar"', default=unicode_default)
        self.assertTrue(unicode_default in result)

    def test_no_slug_given(self):
        "Slug is required by the tag."
        self.assertRaises(TemplateSyntaxError, self.render_template_tag, slug='')

    def test_shared_scribble(self):
        "Render a scribble by the slug url pair."
        self.create_scribble(
            url='/shared/', slug='shared',
            content='<p>Shared scribble content.</p>'
        )
        result = self.render_template_tag(slug='"shared"', url='"/shared/"')
        self.assertTrue('<p>Shared scribble content.</p>' in result)
        # switch context and render the shared scribble
        self.request = self.factory.get('/bar/')
        result = self.render_template_tag(slug='"shared"', url='"/shared/"')
        self.assertTrue('<p>Shared scribble content.</p>' in result)

    @skipIf(not CACHE_TIMEOUT, "Caching is disabled.")
    def test_cache_scribble_lookup(self):
        "DB lookups should be cached."
        cache.clear()
        with self.assertNumQueries(1):
            # Render twice but should be one DB lookup
            result = self.render_template_tag(slug='"sidebar"')
            self.assertTrue('<p>Scribble content.</p>' in result)
            result = self.render_template_tag(slug='"sidebar"')
            self.assertTrue('<p>Scribble content.</p>' in result)

    @skipIf(not CACHE_TIMEOUT, "Caching is disabled.")
    def test_cache_lookup_miss(self):
        "Scribbles not in the DB should also be cached to prevent unnecessary lookup."
        self.scribble.delete()
        cache.clear()
        with self.assertNumQueries(1):
            # Render twice but should be one DB lookup
            result = self.render_template_tag(slug='"sidebar"')
            self.assertTrue('<p>Default.</p>' in result)
            result = self.render_template_tag(slug='"sidebar"')
            self.assertTrue('<p>Default.</p>' in result)

    @skipIf(not CACHE_TIMEOUT, "Caching is disabled.")
    def test_cached_on_save(self):
        "Scribbles are cached on their save."
        cache.clear()
        other_scribble = self.create_scribble(
            url='/foo/', slug='header',
            content='<p>New content.</p>'
        )
        with self.assertNumQueries(0):
            # Render twice but should be one DB lookup
            result = self.render_template_tag(slug='"header"')
            self.assertTrue('<p>New content.</p>' in result)

    def test_unauthenticated_controls(self):
        "Unauthenticated users will not see the scribble controls."
        result = self.render_template_tag(slug='"sidebar"')
        self.assertFalse('<form' in result)
        self.assertFalse('with-controls' in result)

    def test_no_permissions_controls(self):
        "Authenticated users without permissions will not see the scribble controls."
        self.request.user = self.create_user()
        result = self.render_template_tag(slug='"sidebar"')
        self.assertFalse('<form' in result)
        self.assertFalse('with-controls' in result)

    def test_scribble_editor(self):
        "Authenticated users with permission to edit will see the scribble controls."
        change_perm = Permission.objects.get(
            codename='change_scribble',
            content_type__app_label='scribbler',
            content_type__model='scribble',
        )
        user = self.create_user()
        user.user_permissions.add(change_perm)
        self.request.user = user # Fake the auth middleware
        result = self.render_template_tag(slug='"sidebar"')
        self.assertTrue('<form' in result)
        self.assertTrue('with-controls' in result)
        self.assertTrue('{% endscribble %}' not in result)

    def test_scribble_creator(self):
        "Authenticated users with permission to create will see the scribble controls."
        add_perm = Permission.objects.get(
            codename='add_scribble',
            content_type__app_label='scribbler',
            content_type__model='scribble',
        )
        user = self.create_user()
        user.user_permissions.add(add_perm)
        self.request.user = user # Fake the auth middleware
        result = self.render_template_tag(slug='"other"')
        self.assertTrue('<form' in result)
        self.assertTrue('with-controls' in result)


class RenderScribbleFieldTestCase(ScribblerDataTestCase):
    "Tag to render a model field instance scribble."

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/foo/')
        self.user = self.create_user()
        self.days_log = DaysLog.objects.create(happenings=self.get_random_string())

    def render_template_tag(self, model_instance, field_name, context=None):
        "Render the template tag."
        context = context or {}
        context['model_instance'] = model_instance
        template = Template("""
            {{% load scribbler_tags %}}{{% scribble_field model_instance '{0}' %}}
        """.format(field_name))
        context = RequestContext(self.request, context)
        return template.render(context)

    def test_basic_rendering(self):
        "Render a scribble field."
        result = self.render_template_tag(self.days_log, 'happenings')
        self.assertTrue(self.days_log.happenings in result)

    def test_unauthenticated_controls(self):
        "Unauthenticated users will not see the scribble controls."
        result = self.render_template_tag(self.days_log, 'happenings')
        self.assertFalse('<form' in result)
        self.assertFalse('with-controls' in result)

    def test_no_permissions_controls(self):
        "Authenticated users without permissions will not see the scribble controls."
        self.request.user = self.user  # Fake the auth middleware
        result = self.render_template_tag(self.days_log, 'happenings')
        self.assertFalse('<form' in result)
        self.assertFalse('with-controls' in result)

    def test_scribble_editor(self):
        "Authenticated users with permission to edit will see the scribble controls."
        change_perm = Permission.objects.get(
            codename='change_dayslog',
            content_type__app_label='scribbler',
            content_type__model='dayslog',
        )
        self.user.user_permissions.add(change_perm)
        self.request.user = self.user  # Fake the auth middleware
        result = self.render_template_tag(self.days_log, 'happenings')
        self.assertTrue('<form' in result)
        self.assertTrue('with-controls' in result)
