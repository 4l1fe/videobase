# coding: utf-8
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .factories_users_api import UserFactory
from apps.users.models import SessionToken
from apps.users.models import User
from utils.common import random_string


class APIUserTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()

        self.profile = self.user.profile
        self.url_name = ''
        s_token = SessionToken.objects.create(user=self.user)
        self.headers = s_token.key

    def test_api_user_401_post(self):
        if self.url_name:
            response = self.client.post(reverse(self.url_name, kwargs={'format': 'json'}))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class APIUserInfoTestCase(APIUserTestCase):
    def setUp(self):
        super(APIUserInfoTestCase, self).setUp()
        self.url_name = 'users_api:user_info'

    def test_api_user_info_401_get(self):
        response = self.client.get(reverse(self.url_name, kwargs={'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_user_info_get(self):
        response = self.client.get(reverse(self.url_name, kwargs={'format': 'json'}), HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.get_name(), response.data['name'])
        self.assertEqual(self.user.id, response.data['id'])
        self.assertEqual(self.user.email, response.data['email'])

    def test_api_user_info_post_valid_name(self):
        name = 'admin_admin'
        response = self.client.post(reverse(self.url_name, kwargs={'format': 'json'}),
                                    data={'name': name}, HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.profile.get_name(), name)

    def test_api_user_info_post_not_valid_name(self):
        not_valid_name = random_string(size=31)
        response = self.client.post(reverse(self.url_name, kwargs={'format': 'json'}),
                                    data={'name': not_valid_name}, HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=self.user.pk)
        self.assertNotEqual(user.profile.get_name(), not_valid_name)

    def test_api_user_info_post_valid_email(self):
        email = 'wolko_dav@mail.ru'
        response = self.client.post(reverse(self.url_name, kwargs={'format': 'json'}),
                                    data={'email': email}, HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.email, email)

    def test_api_user_info_post_not_valid_email(self):
        not_valid_email = 'admin'
        response = self.client.post(reverse(self.url_name, kwargs={'format': 'json'}),
                                    data={'email': not_valid_email}, HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(pk=self.user.pk)
        self.assertNotEqual(user.email, not_valid_email)

    def test_api_user_info_post_name_email(self):
        name = 'admin_admin'
        email = 'wolko_dav@mail.ru'
        response = self.client.post(reverse(self.url_name, kwargs={'format': 'json'}),
                                    data={'email': email, 'name': name}, HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.email, email)
        self.assertEqual(user.profile.get_name(), name)


class APIUserPasswordTestCase(APIUserTestCase):
    def setUp(self):
        super(APIUserPasswordTestCase, self).setUp()
        self.url_name = 'users_api:user_change_password'

    def test_api_user_password_change_password(self):
        response = self.client.post(reverse(self.url_name, kwargs={'format': 'json'}),
                                    HTTP_X_MI_SESSION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        password = response.data['password']
        response = self.client.post(reverse('users_api:login', kwargs={'format': 'json'}),
                                    data={'username': self.user.username, 'password': password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
