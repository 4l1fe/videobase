# coding: utf-8

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APISimpleTestCase

from apps.casts.tests.factories import UserCastsFactory, UserFactory, CastsFactory


class SubscribeTestCase(APISimpleTestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.cast = CastsFactory.create()
        self.user_cast = UserCastsFactory.create(user=self.user, cast=self.cast)

    def test_search(self):
        response = self.client.get(
            reverse('cast_subscribe_view', kwargs={'cast_id': 1, 'format': 'json'}), data={})

        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)
