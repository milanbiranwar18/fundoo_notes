import json
import pdb
from django.test import TestCase
from django.urls import reverse

from user.models import User
from .test_setup import TestSetUp


class ViewsTestCase(TestSetUp):
    def test_user_registration(self):
        api_response = self.client.post(self.register_url, self.registration_user_data, format="json")
        # pdb.set_trace()            # in terminal give res.data to see all data

        self.assertEqual(api_response.data['data'].get('email'), self.registration_user_data["email"])
        self.assertEqual(api_response.data['data'].get('mob_num'), self.registration_user_data['mob_num'])
        self.assertEqual(api_response.data['data'].get('location'), self.registration_user_data['location'])
        self.assertEqual(api_response.data['data'].get('first_name'), self.registration_user_data['first_name'])
        self.assertEqual(api_response.data['data'].get('last_name'), self.registration_user_data['last_name'])
        self.assertEqual(api_response.data['data'].get('username'), self.registration_user_data['username'])
        self.assertEqual(api_response.data['status'], 201)

    def test_user_login(self):
        self.client.post(self.register_url, self.registration_user_data, format="json")
        log_api_response = self.client.post(self.login_url, self.login_user_data, format="json")
        self.assertEqual(log_api_response.data['status'], 201)


class ViewsTestCaseWithFaker(TestSetUp):
    def test_user_registration(self):
        api_response = self.client.post(self.register_url, self.regist_user_data, format="json")
        # import pdb
        # pdb.set_trace()            # in terminal give res.data to see all data
        # print(api_response.data)
        self.assertEqual(api_response.data['data'].get('email'), self.regist_user_data["email"])
        self.assertEqual(api_response.data['data'].get('mob_num'), self.regist_user_data['mob_num'])
        self.assertEqual(api_response.data['data'].get('location'), self.regist_user_data['location'])
        self.assertEqual(api_response.data['data'].get('first_name'), self.regist_user_data['first_name'])
        self.assertEqual(api_response.data['data'].get('last_name'), self.regist_user_data['last_name'])
        self.assertEqual(api_response.data['data'].get('username'), self.regist_user_data['username'])
        self.assertEqual(api_response.data['status'], 201)


    def test_user_login(self):
        reg_api_response = self.client.post(self.register_url, self.regist_user_data, format="json")
        username = reg_api_response.data['data'].get('username')
        user = User.objects.get(username=username)
        user.is_verified = True
        user.save()
        log_api_response = self.client.post(self.login_url, self.regist_user_data, format="json")
        self.assertEqual(log_api_response.data['status'], 201)


class NoteViewsTestCase(TestSetUp):
    def test_create_note_api(self):
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        create_note_api_response = self.client.post(self.create_note_url, self.create_note_data, format="json")
        self.assertEqual(create_note_api_response.data['status'], 201)

    def test_get_note_api(self):
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        self.client.post(self.create_note_url, self.create_note_data, format="json")
        get_note_api_response = self.client.get(self.get_note_url,  format="json")
        self.assertEqual(get_note_api_response.data['status'], 200)

    def test_update_note_api(self):
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        res = self.client.post(self.create_note_url, self.create_note_data, format="json")
        self.update_note_data.update({"id":  res.data.get("Data").get("id")})
        update_note_api_response = self.client.put(self.update_note_url, self.update_note_data, format="json")
        self.assertEqual(update_note_api_response.data['status'], 200)

    def test_delete_note_api(self):
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        response = self.client.post(self.create_note_url, self.create_note_data, format="json")
        pk = response.data['Data'].get('id')
        self.delete_note_url = reverse('note', args=[pk])
        delete_note_api_response = self.client.delete(self.delete_note_url, format="json")
        self.assertEqual(delete_note_api_response.data['status'], 200)


class LabelViewsTestCase(TestSetUp):
    def test_create_label_api(self):
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        create_label_api_response = self.client.post(self.create_label_url, self.create_label_data, format="json")
        self.assertEqual(create_label_api_response.data['status'], 201)

    def test_get_label_api(self):
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        self.client.post(self.create_label_url, self.create_label_data, format="json")
        get_label_api_response = self.client.get(self.get_label_url,  format="json")
        self.assertEqual(get_label_api_response.data['status'], 200)

    def test_update_label_api(self):
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        res = self.client.post(self.create_label_url, self.create_label_data, format="json")
        pk = res.data['data'].get('id')
        self.update_label_url = reverse('label_ruc', args=[pk])
        update_label_api_response = self.client.put(self.update_label_url, self.update_label_data, format="json")
        self.assertEqual(update_label_api_response.data['status'], 200)

    def test_delete_label_api(self):
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        response = self.client.post(self.create_label_url, self.create_label_data, format="json")
        pk = response.data['data'].get('id')
        self.delete_label_url = reverse('label_ruc', args=[pk])
        delete_label_api_response = self.client.delete(self.delete_label_url, format="json")
        self.assertEqual(delete_label_api_response.data['status'], 200)


class IsArchiveViewsTestCase(TestSetUp):

    def test_is_archive_api(self):
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        res = self.client.post(self.create_note_url, self.create_note_data, format="json")
        pk = res.data['Data'].get('id')
        self.is_archive_url = reverse('archive', args=[pk])
        is_archive_api_response = self.client.put(self.is_archive_url, format="json")
        self.assertEqual(is_archive_api_response.data['status'], 200)

    def test_get_is_archive_api(self):
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        res = self.client.post(self.create_note_url, self.create_note_data, format="json")
        pk = res.data['Data'].get('id')
        self.is_archive_url = reverse('archive', args=[pk])
        self.client.put(self.is_archive_url, format="json")
        get_isarchive_response = self.client.get(self.get_is_archive_url,  format="json")
        self.assertEqual(get_isarchive_response.data['status'], 200)


class IsTrashViewsTestCase(TestSetUp):

    def test_is_trash_api(self):
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        res = self.client.post(self.create_note_url, self.create_note_data, format="json")
        pk = res.data['Data'].get('id')
        self.is_trash_url = reverse('trash', args=[pk])
        is_trash_api_response = self.client.put(self.is_trash_url, format="json")
        self.assertEqual(is_trash_api_response.data['status'], 200)

    def test_get_is_trash_api(self):
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        res = self.client.post(self.create_note_url, self.create_note_data, format="json")
        pk = res.data['Data'].get('id')
        self.is_trash_url = reverse('trash', args=[pk])
        self.client.put(self.is_trash_url, format="json")
        get_trash_api_response = self.client.get(self.get_is_trash_url,  format="json")
        self.assertEqual(get_trash_api_response.data['status'], 200)


class CollaboratorViewsTestCase(TestSetUp):
    def test_add_collaborator_api(self):
        api_response = self.client.post(self.register_url, self.regist_user_data, format="json")
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        res = self.client.post(self.create_note_url, self.create_note_data, format="json")
        pk = res.data['Data'].get('id')
        self.add_collaborator_data = {
            "collaborator": [api_response.data.get("data").get("username")]
        }
        self.collaborator_url = reverse('collaborator', args=[pk])
        add_collaborator_response = self.client.post(self.collaborator_url, self.add_collaborator_data, format="json")
        self.assertEqual(add_collaborator_response.data['status'], 201)

    def test_delete_collaborator_api(self):
        api_response = self.client.post(self.register_url, self.regist_user_data, format="json")
        self.client.post(self.register_url, self.registration_user_data, format="json")
        self.client.post(self.login_url, self.login_user_data, format="json")
        res = self.client.post(self.create_note_url, self.create_note_data, format="json")
        pk = res.data['Data'].get('id')
        self.add_collaborator_data = {
            "collaborator": [api_response.data.get("data").get("username")]
        }
        self.collaborator_url = reverse('collaborator', args=[pk])
        self.client.post(self.collaborator_url, self.add_collaborator_data, format="json")
        delete_collaborator_response = self.client.delete(self.collaborator_url, self.add_collaborator_data, format="json")
        self.assertEqual(delete_collaborator_response.data['status'], 200)


