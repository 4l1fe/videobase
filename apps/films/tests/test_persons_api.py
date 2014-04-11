from apps.films.views import PersonAPIView
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase



class PersonsTest(APITestCase):
    def test_view(self):
        response = self.client.get('/person/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
