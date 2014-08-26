#coding: utf-8

from rest_framework.test import APISimpleTestCase
from apps.casts.tests.factories import UserCastsFactory, UserFactory, CastsFactory, CastsChatFactory 
from rest_framework.reverse import reverse
from rest_framework import status

from apps.casts.models import UsersCasts, Casts
import ipdb

from rest_framework.authtoken.models import Token
from apps.users.models.api_session import SessionToken, UsersApiSessions

class RatingTestCase(APISimpleTestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.cast = CastsFactory.create(tags =[])

        self.cast_chat = CastsChatFactory.create( cast = self.cast)

        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        self.headers = s_token.key


    def test_rating(self):

        COMM_TEXT = 'Commentary text'

        response = self.client.post(reverse('cast_rating_view',
                                kwargs={'cast_id':self.cast_chat.id, 'format':'json'}
                            ),  HTTP_X_MI_SESSION=self.headers, data = {'rating':5})


        self.assertEqual(response.status_code , status.HTTP_200_OK)


        uc =UsersCasts.objects.get(cast__id=self.cast.id)

        self.assertEqual(uc.rating, 5)

        