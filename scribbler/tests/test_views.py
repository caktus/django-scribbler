"Tests for preview/save views."
from __future__ import unicode_literals

from datetime import date

from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

from .base import ScribblerDataTestCase, Scribble


class BaseViewTestCase(ScribblerDataTestCase):
    "Common functionality for testing views."

    urls = "scribbler.tests.urls"

    def setUp(self):
        self.user = self.create_user(username='test', password='test')
        self.client.login(username='test', password='test')
        self.change_perm = Permission.objects.get(
            codename='change_scribble', 
            content_type__app_label='scribbler', 
            content_type__model='scribble',
        )
        self.add_perm = Permission.objects.get(
            codename='add_scribble', 
            content_type__app_label='scribbler', 
            content_type__model='scribble',
        )
        self.delete_perm = Permission.objects.get(
            codename='delete_scribble', 
            content_type__app_label='scribbler', 
            content_type__model='scribble',
        )
        self.user.user_permissions.add(self.change_perm)
        self.user.user_permissions.add(self.add_perm)
        self.user.user_permissions.add(self.delete_perm)


class PreviewTestCase(BaseViewTestCase):
    "Previewing scribbler content."

    def setUp(self):
        super(PreviewTestCase, self).setUp()
        self.url = reverse('preview-scribble')

    def get_valid_data(self):
        "Base valid data."
        data = {
            'slug': 'test',
            'url': '/',
            'content': '{% now "Y" %}'
        }
        return data

    def test_post_required(self):
        "Preview view requires a POST."
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405, "GET should not be allowed.")

    def test_valid_response(self):
        "Rendered content should be given in the response."
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertTrue(results['valid'])
        self.assertFalse('error' in results)
        self.assertEqual(results['html'], "{0}".format(date.today().year))

    def test_invalid_template(self):
        "Debug info should be given if the template content was invalid."
        data = self.get_valid_data()
        data['content'] = '{% now %}'
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertFalse(results['valid'])
        self.assertEqual(results['html'], '')
        self.assertEqual(results['error']['line'], 1)

    def test_login_required(self):
        "Return 403 if user is not authenticated."
        self.client.logout()
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_permission_required(self):
        "Return 403 if user is does not have permissions to preview scribbles."
        self.user.user_permissions.remove(self.change_perm)
        self.user.user_permissions.remove(self.add_perm)
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 403)


class CreateTestCase(BaseViewTestCase):
    "Creating a new scribble."

    def setUp(self):
        super(CreateTestCase, self).setUp()
        self.url = reverse('create-scribble')

    def get_valid_data(self):
        "Base valid data."
        data = {
            'slug': 'test',
            'url': '/',
            'content': '{% now "Y" %}'
        }
        return data

    def test_post_required(self):
        "Create view requires a POST."
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405, "GET should not be allowed.")

    def test_valid_response(self):
        "Save new scribble data."
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertTrue(results['valid'])
        pk = results['id']
        scribble = Scribble.objects.get(pk=pk)
        self.assertEqual(scribble.content, data['content'])

    def test_invalid_template(self):
        "Data should not be saved if the template is invalid."
        data = self.get_valid_data()
        data['content'] = '{% now %}'
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertFalse(results['valid'])
        self.assertEqual(results['id'], None)
        self.assertEqual(Scribble.objects.count(), 0)

    def test_login_required(self):
        "Return 403 if user is not authenticated."
        self.client.logout()
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_permission_required(self):
        "Return 403 if user is does not have permissions to create scribbles."
        self.user.user_permissions.remove(self.add_perm)
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 403)


class EditTestCase(BaseViewTestCase):
    "Edit an existing scribble."

    def setUp(self):
        super(EditTestCase, self).setUp()
        self.scribble = self.create_scribble()
        self.url = reverse('edit-scribble', kwargs={'scribble_id': self.scribble.pk})

    def get_valid_data(self):
        "Base valid data."
        data = {
            'content': '{% now "Y" %}'
        }
        return data

    def test_post_required(self):
        "Edit view requires a POST."
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405, "GET should not be allowed.")

    def test_valid_response(self):
        "Edit an existing scribble."
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertTrue(results['valid'])
        self.assertEqual(results['id'], self.scribble.pk)
        scribble = Scribble.objects.get(pk=self.scribble.pk)
        self.assertEqual(scribble.content, data['content'])

    def test_invalid_template(self):
        "Data should not be saved if the template is invalid."
        data = self.get_valid_data()
        data['content'] = '{% now %}'
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertFalse(results['valid'])
        self.assertEqual(results['id'], None)
        scribble = Scribble.objects.get(pk=self.scribble.pk)
        self.assertNotEqual(scribble.content, data['content'])

    def test_invalid_pk(self):
        "404 is returned if unknown pk is given."
        self.scribble.delete()
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 404)

    def test_login_required(self):
        "Return 403 if user is not authenticated."
        self.client.logout()
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_permission_required(self):
        "Return 403 if user is does not have permissions to edit the scribble."
        self.user.user_permissions.remove(self.change_perm)
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 403)


class DeleteTestCase(BaseViewTestCase):
    "Delete an existing scribble."

    def setUp(self):
        super(DeleteTestCase, self).setUp()
        self.scribble = self.create_scribble()
        self.url = self.scribble.get_delete_url()

    def get_valid_data(self):
        "Base valid data."
        return {}

    def test_post_required(self):
        "Delete view requires a POST."
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405, "GET should not be allowed.")

    def test_valid_response(self):
        "Delete an existing scribble."
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertRaises(Scribble.DoesNotExist, Scribble.objects.get, pk=self.scribble.pk)

    def test_invalid_pk(self):
        "404 is returned if unknown pk is given."
        self.scribble.delete()
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 404)

    def test_login_required(self):
        "Return 403 if user is not authenticated."
        self.client.logout()
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_permission_required(self):
        "Return 403 if user is does not have permissions to delete the scribble."
        self.user.user_permissions.remove(self.delete_perm)
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 403)
