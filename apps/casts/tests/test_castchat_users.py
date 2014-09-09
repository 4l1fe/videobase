# coding: utf-8
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APISimpleTestCase

from apps.casts.models import CastsChatsMsgs, CastsChats
from apps.casts.tests.factories import UserCastsFactory, UserFactory, CastsFactory, CastsChatFactory

from apps.users.models import SessionToken


class CastChatMsgSendTestCase(APISimpleTestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.cast = CastsFactory.create(tags=[])
        self.user_cast = UserCastsFactory(user=self.user, cast=self.cast)

        self.cast_chat = CastsChatFactory._get_or_create(CastsChats, cast=self.cast, status=1)

        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        self.headers = s_token.key

    def test_send(self):
        COMM_TEXT = u'Commentary text'
        response = self.client.post(
            reverse('castchat_send_view', kwargs={'cast_id': self.cast_chat.id, 'format': 'json'}),
            HTTP_X_MI_SESSION=self.headers, data={'text': COMM_TEXT})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ccm = CastsChatsMsgs.objects.get(cast__id=self.cast_chat.cast.id)
        self.assertEqual(ccm.text, COMM_TEXT)
