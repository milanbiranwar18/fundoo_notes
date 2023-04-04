from django.urls import reverse

from user.models import User
from .test_setup import TestSetUp

register_url = reverse('registration')
login_url = reverse('login')


class ViewsTestCase(TestSetUp):
    def test_user_registration(self):
        api_response = self.client.post(register_url, self.registration_user_data, format="json")
        # pdb.set_trace()            # in terminal give res.data to see all data

        self.assertEqual(api_response.data['data'].get('email'), self.registration_user_data["email"])
        self.assertEqual(api_response.data['data'].get('mob_num'), self.registration_user_data['mob_num'])
        self.assertEqual(api_response.data['data'].get('location'), self.registration_user_data['location'])
        self.assertEqual(api_response.data['data'].get('first_name'), self.registration_user_data['first_name'])
        self.assertEqual(api_response.data['data'].get('last_name'), self.registration_user_data['last_name'])
        self.assertEqual(api_response.data['data'].get('username'), self.registration_user_data['username'])
        self.assertEqual(api_response.data['status'], 201)

    def test_empty_user_registration_data(self):
        api_response = self.client.post(register_url, self.empty_registration_user_data, format="json")
        self.assertEqual(api_response.status_code, 400)

    def test_invalid_user_registration(self):
        api_response = self.client.post(register_url, self.invalid_registration_user_data, format="json")
        self.assertEqual(api_response.status_code, 400)

    def test_user_login(self):
        self.client.post(register_url, self.registration_user_data, format="json")
        log_api_response = self.client.post(login_url, self.login_user_data, format="json")
        self.assertEqual(log_api_response.data['status'], 201)

    def test_empty_user_login_data(self):
        self.client.post(register_url, self.registration_user_data, format="json")
        log_api_response = self.client.post(login_url, self.empty_login_user_data, format="json")
        self.assertEqual(log_api_response.status_code, 400)

    def test_invalid_user_login(self):
        self.client.post(register_url, self.registration_user_data, format="json")
        log_api_response = self.client.post(login_url, self.invalid_login_user_data, format="json")
        self.assertEqual(log_api_response.status_code, 400)


class ViewsTestCaseWithFaker(TestSetUp):
    def test_user_registration(self):
        api_response = self.client.post(register_url, self.regist_user_data, format="json")
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
        reg_api_response = self.client.post(register_url, self.regist_user_data, format="json")
        username = reg_api_response.data['data'].get('username')
        user = User.objects.get(username=username)
        user.is_verified = True
        user.save()
        log_api_response = self.client.post(login_url, self.regist_user_data, format="json")
        self.assertEqual(log_api_response.data['status'], 201)


def authenticate(client, registration_user_data, login_user_data):
    client.post(register_url, registration_user_data, format="json")
    res = client.post(login_url, login_user_data, format="json")
    token = res.data.get("token")
    headers = {
        "HTTP_TOKEN": token
    }
    return headers


class NoteViewsTestCase(TestSetUp):
    def test_create_note_api(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        create_note_api_response = self.client.post(self.note_url, self.create_note_data, **headers)
        self.assertEqual(create_note_api_response.data['status'], 201)

    def test_create_note_api_with_empty_data(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        create_note_api_response = self.client.post(self.note_url, self.create_empty_note_data, **headers)
        self.assertEqual(create_note_api_response.status_code, 400)

    def test_create_note_api_with_invalid_data(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        create_note_api_response = self.client.post(self.note_url, self.create_note_data_with_invalid, **headers)
        self.assertEqual(create_note_api_response.status_code, 400)

    def test_get_note_api(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        self.client.post(self.note_url, self.create_note_data, **headers)
        get_note_api_response = self.client.get(self.note_url, **headers)
        self.assertEqual(get_note_api_response.data['status'], 200)

    def test_get_note_without_creating_note(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        get_note_api_response = self.client.get(self.note_url, **headers)
        self.assertNotEqual(get_note_api_response.status_code, 400)

    def test_update_note_api(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        res = self.client.post(self.note_url, self.create_note_data, **headers)
        self.update_note_data.update({"id": res.data.get("Data").get("id")})
        update_note_api_response = self.client.put(self.note_url, self.update_note_data, **headers)
        self.assertEqual(update_note_api_response.status_code, 200)

    def test_update_note_api_with_empty_data(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        res = self.client.post(self.note_url, self.create_empty_note_data, **headers)
        # self.update_note_data.update({"id": res.data.get("Data").get("id")})
        update_note_api_response = self.client.put(self.note_url, self.update_note_data, **headers)
        self.assertEqual(update_note_api_response.status_code, 400)

    def test_update_note_api_without_created_note(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        # res = self.client.post(self.note_url, **headers)
        # self.update_note_data.update({"id": res.data.get("Data").get("id")})
        update_note_api_response = self.client.put(self.note_url, self.update_note_data, **headers)
        self.assertEqual(update_note_api_response.status_code, 400)

    def test_update_note_api_with_invalid_note_tata(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        res = self.client.post(self.note_url, self.create_note_data, **headers)
        self.update_note_data.update({"id": res.data.get("Data").get("id")})
        update_note_api_response = self.client.put(self.note_url, self.create_note_data_with_invalid, **headers)
        self.assertEqual(update_note_api_response.status_code, 400)

    def test_delete_note_api(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        response = self.client.post(self.note_url, self.create_note_data, **headers)
        pk = response.data['Data'].get('id')
        self.delete_note_url = reverse('rd_note', args=[pk])
        delete_note_api_response = self.client.delete(self.delete_note_url, **headers)
        self.assertEqual(delete_note_api_response.data['status'], 200)

    def test_delete_note_api_with_invalid_id(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        response = self.client.post(self.note_url, self.create_note_data, **headers)
        pk = response.data['Data'].get('id')
        self.delete_note_url = reverse('rd_note', args=[32])
        delete_note_api_response = self.client.delete(self.delete_note_url, **headers)
        self.assertEqual(delete_note_api_response.status_code, 400)


class LabelViewsTestCase(TestSetUp):
    def test_create_label_api(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        create_label_api_response = self.client.post(self.label_url, self.create_label_data, **headers, format="json")
        self.assertEqual(create_label_api_response.data['status'], 201)

    def test_get_label_api(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        self.client.post(self.label_url, self.create_label_data, **headers, format="json")
        get_label_api_response = self.client.get(self.label_url, **headers, format="json")
        self.assertEqual(get_label_api_response.data['status'], 200)

    def test_update_label_api(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        res = self.client.post(self.label_url, self.create_label_data, **headers, format="json")
        pk = res.data['data'].get('id')
        self.update_label_url = reverse('label_ruc', args=[pk])
        update_label_api_response = self.client.put(self.update_label_url, self.update_label_data, **headers,
                                                    format="json")
        self.assertEqual(update_label_api_response.data['status'], 200)

    def test_update_label_with_invalid_id(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        res = self.client.post(self.label_url, self.update_label_data_with_invalid_id, **headers, format="json")
        pk = res.data['data'].get('id')
        self.update_label_url = reverse('label_ruc', args=[12])
        update_label_api_response = self.client.put(self.update_label_url, self.update_label_data, **headers,
                                                    format="json")
        self.assertEqual(update_label_api_response.status_code, 400)

    def test_delete_label_api(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        response = self.client.post(self.label_url, self.create_label_data, **headers, format="json")
        pk = response.data['data'].get('id')
        self.delete_label_url = reverse('label_ruc', args=[pk])
        delete_label_api_response = self.client.delete(self.delete_label_url, **headers, format="json")
        self.assertEqual(delete_label_api_response.data['status'], 200)

    def test_delete_label_with_invalid_id(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        response = self.client.post(self.label_url, self.create_label_data, **headers, format="json")
        pk = response.data['data'].get('id')
        self.delete_label_url = reverse('label_ruc', args=[12])
        delete_label_api_response = self.client.delete(self.delete_label_url, **headers, format="json")
        self.assertEqual(delete_label_api_response.status_code, 400)


class IsArchiveViewsTestCase(TestSetUp):

    def test_is_archive_api(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        res = self.client.post(self.note_url, self.create_note_data, **headers, format="json")
        pk = res.data['Data'].get('id')
        self.is_archive_url = reverse('archive', args=[pk])
        is_archive_api_response = self.client.put(self.is_archive_url, **headers, format="json")
        self.assertEqual(is_archive_api_response.data['status'], 200)

    def test_is_archive_with_invalid_id(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        res = self.client.post(self.note_url, self.create_note_data, **headers, format="json")
        pk = res.data['Data'].get('id')
        self.is_archive_url = reverse('archive', args=[12])
        is_archive_api_response = self.client.put(self.is_archive_url, **headers, format="json")
        self.assertEqual(is_archive_api_response.status_code, 400)

    def test_get_is_archive_api(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        res = self.client.post(self.note_url, self.create_note_data, **headers, format="json")
        pk = res.data['Data'].get('id')
        self.is_archive_url = reverse('archive', args=[pk])
        self.client.put(self.is_archive_url, format="json")
        get_isarchive_response = self.client.get(self.get_is_archive_url, **headers, format="json")
        self.assertEqual(get_isarchive_response.data['status'], 200)




class IsTrashViewsTestCase(TestSetUp):

    def test_is_trash_api(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        res = self.client.post(self.note_url, self.create_note_data, **headers, format="json")
        pk = res.data['Data'].get('id')
        self.is_trash_url = reverse('trash', args=[pk])
        is_trash_api_response = self.client.put(self.is_trash_url, **headers, format="json")
        self.assertEqual(is_trash_api_response.data['status'], 200)

    def test_get_is_trash_api(self):
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        res = self.client.post(self.note_url, self.create_note_data, **headers, format="json")
        pk = res.data['Data'].get('id')
        self.is_trash_url = reverse('trash', args=[pk])
        self.client.put(self.is_trash_url, format="json")
        get_trash_api_response = self.client.get(self.get_is_trash_url, **headers, format="json")
        self.assertEqual(get_trash_api_response.data['status'], 200)


class CollaboratorViewsTestCase(TestSetUp):
    def test_add_collaborator_api(self):
        api_response = self.client.post(register_url, self.regist_user_data, format="json")
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        res = self.client.post(self.note_url, self.create_note_data, **headers, format="json")
        pk = res.data['Data'].get('id')
        self.add_collaborator_data = {
            "collaborator": [api_response.data.get("data").get("username")]
        }
        self.collaborator_url = reverse('collaborator', args=[pk])
        add_collaborator_response = self.client.post(self.collaborator_url, self.add_collaborator_data, **headers,
                                                     format="json")
        self.assertEqual(add_collaborator_response.data['status'], 201)

    def test_delete_collaborator_api(self):
        api_response = self.client.post(register_url, self.regist_user_data, format="json")
        headers = authenticate(client=self.client, registration_user_data=self.registration_user_data,
                               login_user_data=self.login_user_data)
        res = self.client.post(self.note_url, self.create_note_data, **headers, format="json")
        pk = res.data['Data'].get('id')
        self.add_collaborator_data = {
            "collaborator": [api_response.data.get("data").get("username")]
        }
        self.collaborator_url = reverse('collaborator', args=[pk])
        self.client.post(self.collaborator_url, self.add_collaborator_data, format="json")
        delete_collaborator_response = self.client.delete(self.collaborator_url, self.add_collaborator_data, **headers,
                                                          format="json")
        self.assertEqual(delete_collaborator_response.data['status'], 200)

