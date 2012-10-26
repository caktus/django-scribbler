"Tests for preview/save views."
from __future__ import unicode_literals

from datetime import date

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils import simplejson as json

from . import DaysLog
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
        self.change_dayslog_perm = Permission.objects.get(
            codename='change_dayslog',
            content_type__app_label='scribbler',
            content_type__model='dayslog',
        )
        self.user.user_permissions.add(self.change_perm)
        self.user.user_permissions.add(self.add_perm)
        self.user.user_permissions.add(self.delete_perm)
        self.user.user_permissions.add(self.change_dayslog_perm)


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

    def test_preview_existing(self):
        "Preview content for a scribble which exists. See #34."
        data = self.get_valid_data()
        scribble = self.create_scribble(**data)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertTrue(results['valid'])
        self.assertFalse('error' in results)


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
        scribble = Scribble.objects.get(slug=data['slug'], url=data['url'])
        self.assertEqual(scribble.content, data['content'])

    def test_invalid_template(self):
        "Data should not be saved if the template is invalid."
        data = self.get_valid_data()
        data['content'] = '{% now %}'
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertFalse(results['valid'])
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


class EditFieldTestCase(BaseViewTestCase):
    "Edit a model instance field via scribbler."
    url_name = 'edit-scribble-field'

    def setUp(self):
        self.days_log = DaysLog.objects.create(happenings=self.get_random_string())
        super(EditFieldTestCase, self).setUp()
        self.url = reverse(self.url_name, kwargs=self.get_valid_kwargs())

    def get_valid_data(self):
        data = {
            'content': self.get_random_string(),
        }
        return data

    def get_valid_kwargs(self):
        return {
            'ct_pk': ContentType.objects.get_for_model(self.days_log).pk,
            'instance_pk': self.days_log.pk,
            'field_name': 'happenings',
        }

    def test_post_required(self):
        "Edit field view requires a POST."
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405, "GET should not be allowed.")

    def test_successful_edit(self):
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertTrue(results['valid'])
        days_log = DaysLog.objects.get(pk=self.days_log.pk)
        self.assertEqual(days_log.happenings, data['content'])

    def test_field_validation_failure(self):
        data = {
            'content': '',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertFalse(results['valid'])
        self.assertTrue('error' in results)
        err_info = results['error']
        self.assertTrue('message' in err_info)
        self.assertTrue('required' in err_info['message'], err_info['message'])
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.username, self.user.username)

    def test_model_validation_failure(self):
        log2 = DaysLog.objects.create(happenings="Duplicate value")
        data = {
            'content': log2.happenings,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertFalse(results['valid'])
        self.assertTrue('error' in results)
        err_info = results['error']
        self.assertTrue('message' in err_info)
        self.assertTrue('already exists' in err_info['message'], err_info['message'])
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.username, self.user.username)

    def test_invalid_ct_pk(self):
        kwargs = self.get_valid_kwargs()
        kwargs['ct_pk'] = ContentType.objects.order_by('-id')[0].pk + 1
        url = reverse(self.url_name, kwargs=kwargs)
        response = self.client.post(url, data=self.get_valid_data())
        self.assertEqual(response.status_code, 404)

    def test_invalid_instance_pk(self):
        kwargs = self.get_valid_kwargs()
        kwargs['instance_pk'] = User.objects.order_by('-id')[0].pk + 1
        url = reverse(self.url_name, kwargs=kwargs)
        response = self.client.post(url, data=self.get_valid_data())
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertFalse(results['valid'])
        self.assertTrue('error' in results)
        err_info = results['error']
        self.assertTrue('message' in err_info)
        self.assertTrue('does not exist' in err_info['message'], err_info['message'])

    def test_invalid_field_name(self):
        kwargs = self.get_valid_kwargs()
        kwargs['field_name'] = 'ussserrname'
        url = reverse(self.url_name, kwargs=kwargs)
        response = self.client.post(url, data=self.get_valid_data())
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content.decode('utf-8'))
        self.assertFalse(results['valid'])
        self.assertTrue('error' in results)
        err_info = results['error']
        self.assertTrue('message' in err_info)
        self.assertTrue('has no field named' in err_info['message'], err_info['message'])

    def test_login_required(self):
        "Return 403 if user is not authenticated."
        self.client.logout()
        data = self.get_valid_data()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_permission_required(self):
        "Return 403 if user is does not have permissions to edit the scribble."
        self.user.user_permissions.remove(self.change_dayslog_perm)
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
