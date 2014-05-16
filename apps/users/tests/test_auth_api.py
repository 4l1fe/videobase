#coding: utf-8

from apps.users.tests.factories_auth_api import UserFactory
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from apps.users.models.api_session import *
from rest_framework import status


class AuthTest(APITestCase):
    def setUp(self):
        self.user_factory = UserFactory.create()
        self.token = Token.objects.get(user=self.user_factory)
        self.s_token = SessionToken.objects.create(user=self.user_factory)

    def test_session_token(self):
        UsersApiSessions.objects.create(token=self.s_token)

        headers = self.s_token.key
        response = self.client.get(reverse('session', kwargs={'format': 'json'}), HTTP_X_MI_SESSION=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        headers = response.data['session_token']
        response = self.client.get(reverse('session', kwargs={'format': 'json'}), HTTP_X_MI_SESSION=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_session_token_unauthorized(self):
        headers = "%s %s" % ('X-VB-Token', '0')
        response = self.client.get(reverse('session', kwargs={'format': 'json'}), HTTP_X_MI_SESSION=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_session_token_delete(self):
        UsersApiSessions.objects.create(token=self.s_token)

        headers = self.s_token.key
        response = self.client.get(reverse('session', kwargs={'format': 'json'}), HTTP_X_MI_SESSION=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        headers = response.data['session_token']
        self.client.delete(reverse('session', kwargs={'format': 'json'}), HTTP_X_MI_SESSION=headers)

        response = self.client.get(reverse('session', kwargs={'format': 'json'}), HTTP_X_MI_SESSION=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_session_revoke(self):
        UsersApiSessions.objects.create(token=self.s_token)

        headers = self.s_token.key
        response = self.client.get(reverse('session', kwargs={'format': 'json'}), HTTP_X_MI_SESSION=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        headers = response.data['session_token']
        response = self.client.get(reverse('revoke', kwargs={'format': 'json'}), HTTP_X_MI_SESSION=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('session', kwargs={'format': 'json'}), HTTP_X_MI_SESSION=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        headers = self.s_token.key
        response = self.client.get(reverse('session', kwargs={'format': 'json'}), HTTP_X_MI_SESSION=headers)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

