from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from faker import Faker


class TestSetUp(APITestCase):

    def setUp(self):
        self.note_url = reverse('note')
        self.label_url = reverse('label_lc')
        self.get_is_archive_url = reverse('archive')
        self.get_is_trash_url = reverse('trash')

        self.registration_user_data = {
            'email': 'email@gmail.com',
            'username': "milan",
            'password': "milan",
            "first_name": "milan",
            "last_name": "biranwar",
            "location": "pune",
            "mob_num": 981234567

        }

        self.empty_registration_user_data = {}

        self.invalid_registration_user_data = {
            'email': 'email@gmail.com',
            'username': 123,
            "last_name": "biranwar",
            "location": "pune",
            "mob_num": "981234567"
        }


        self.fake = Faker()
        self.regist_user_data = {
            'email': self.fake.email(),
            'username': self.fake.email(),
            'password': self.fake.password(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "location": self.fake.city(),
            "mob_num": 985698
        }

        self.login_user_data = {
            'username': "milan",
            'password': "milan",
        }

        self.empty_login_user_data = {}

        self.invalid_login_user_data = {
             'email': 'email@gmail.com',
            'password': "milan",
        }

        self.create_note_data = {
            "title": "u have meet tomorrow",
            "description": "do attained",
        }

        self.create_empty_note_data = {}

        self.create_note_data_with_invalid = {
            "title": 123,
            'password': "milan",
        }

        self.update_note_data = {
            "title": "ur meet cancelled",
            "description": "no need to attained",
        }

        self.create_label_data = {
            "label_name": "meeting"
        }

        self.update_label_data_with_invalid_id = {"label_name": "meeting cancelled"}

        self.update_label_data = {
            "label_name": "meeting cancelled"
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()


