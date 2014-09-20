# coding: utf-8
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APISimpleTestCase
from rest_framework.authtoken.models import Token

from apps.casts.models import Casts
from apps.casts.tests.factories import UserFactory, CastsFactory

from apps.users.models import SessionToken


class CastListTestCase(APISimpleTestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.cast = CastsFactory.create(tags=[])

        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        self.headers = s_token.key

    def test_list(self):
        response = self.client.get(
            reverse('casts_api:cast_list_view', kwargs={'format': 'json'}),
            HTTP_X_MI_SESSION=self.headers, data={'text': 'Football'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ccm = Casts.objects.get(pk=self.cast.id)
        self.assertEqual(ccm.title_orig, 'Football')
