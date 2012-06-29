"Tests for preview/save views."

from datetime import date

from django.core.urlresolvers import reverse
from django.utils import simplejson as json

from .base import ScribblerDataTestCase


class BaseViewTestCase(ScribblerDataTestCase):
    "Common functionality for testing views."

    urls = "scribbler.tests.urls"


class PreviewTestCase(BaseViewTestCase):
    "Previewing scribbler content."

    def setUp(self):
        self.url = reverse('preview-scribble')

    def test_post_required(self):
        "Preview view requires a POST."
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405, "GET should not be allowed.")

    def test_valid_response(self):
        "Rendered content should be given in the response."
        data = {
            'slug': 'test',
            'url': '/',
            'content': '{% now "Y" %}'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertTrue(results['valid'])
        self.assertFalse('error' in results)
        self.assertEqual(results['html'], "{0}".format(date.today().year))

    def test_invalid_template(self):
        "Debug info should be given if the template content was invalid."
        data = {
            'slug': 'test',
            'url': '/',
            'content': '{% now %}'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)
        self.assertFalse(results['valid'])
        self.assertEqual(results['html'], '')
        self.assertEqual(results['error']['line'], 1)
