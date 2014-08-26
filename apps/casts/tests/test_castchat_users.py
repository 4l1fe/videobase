#coding: utf-8
#coding: utf-8
from rest_framework.test import APISimpleTestCase
from apps.casts.tests.factories import UserCastsFactory, UserFactory, CastsFactory, CastsChatFactory 
from rest_framework.reverse import reverse
from rest_framework import status

from apps.casts.models import CastsChatsMsgs
import ipdb

from rest_framework.authtoken.models import Token
from apps.users.models.api_session import SessionToken, UsersApiSessions

class CastChatMsgSendTestCase(APISimpleTestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.cast = CastsFactory.create(tags =[])
        self.user_cast = UserCastsFactory(user = self.user, cast = self.cast)
        
        self.cast_chat = CastsChatFactory.create( cast = self.cast)

        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        self.headers = s_token.key


    def test_send(self):

        COMM_TEXT = 'Commentary text'

        response = self.client.post(reverse('castchat_send_view',
                                kwargs={'cast_id':self.cast_chat.id, 'format':'json'}
                            ),  HTTP_X_MI_SESSION=self.headers, data = {'text':COMM_TEXT})


        self.assertEqual(response.status_code , status.HTTP_200_OK)


        ccm = CastsChatsMsgs.objects.get(cast__id=self.cast_chat.cast.id)

        self.assertEqual(ccm.text, COMM_TEXT)

