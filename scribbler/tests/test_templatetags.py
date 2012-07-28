"Test for template tags."

from django.core.cache import cache
from django.template import Template, TemplateSyntaxError
from django.template.context import RequestContext
from django.test.client import RequestFactory
from django.utils.unittest import skipIf

from .base import ScribblerDataTestCase
from scribbler.conf import CACHE_TIMEOUT


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

    def render_template_tag(self, slug, context=None, default='<p>Default.</p>'):
        "Render the template tag."
        context = context or {}
        template = Template("""
            {{% load scribbler_tags %}}{{% scribble {0} %}}{1}{{% endscribble %}}
        """.format(slug, default))
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

    def test_no_slug_given(self):
        "Slug is required by the tag."
        self.assertRaises(TemplateSyntaxError, self.render_template_tag, slug='')

    @skipIf(not CACHE_TIMEOUT, u"Caching is disabled.")
    def test_cache_scribble_lookup(self):
        "DB lookups should be cached."
        cache.clear()
        with self.assertNumQueries(1):
            # Render twice but should be one DB lookup
            result = self.render_template_tag(slug='"sidebar"')
            self.assertTrue('<p>Scribble content.</p>' in result)
            result = self.render_template_tag(slug='"sidebar"')
            self.assertTrue('<p>Scribble content.</p>' in result)

    @skipIf(not CACHE_TIMEOUT, u"Caching is disabled.")
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

    @skipIf(not CACHE_TIMEOUT, u"Caching is disabled.")
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
