#coding: utf-8
from apps.films.api import DetailFilmView

__author__ = 'ipatov'
from apps.films.tests.factories import PersonFactory, FilmFactory
# from apps.films.views import PersonAPIView
# from rest_framework.test import APIRequestFactory
# from rest_framework.test import APIClient
# from rest_framework.authtoken.models import Token
# from django.core.urlresolvers import reverse
#
from rest_framework import status
# from rest_framework.test import APITestCase
# from rest_framework.test import APIRequestFactory
# from rest_framework.test import APIClient
#
#
# class FilmsTest(APITestCase):
#     def test_detail_film_view(self):
#         film = FilmFactory.create()
#         # factory = APIRequestFactory()
#         #response1 = self.client.get(reverse('film_details_view', kwargs={'film_id': 1, 'format': 1}))
#
#         # response = factory.get('api/v1/films/1.json')
#         # response = self.client.get(reverse('api/v1/films/1.json'))
#
#
#         client = APIClient()
#         result = client.get('api/v1/films/1.json')
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         #self.assertContains(response, film.name)


from django.test import TestCase
from rest_framework.reverse import reverse



class FilmsTest(TestCase):

    def setUp(self):
        film = FilmFactory.create()


    def test_api_detail(self):
        response = self.client.get(reverse('film_details_view', kwargs={'film_id': 1, 'format': 'json'}))


        self.assertEqual(response.status_code, status.HTTP_200_OK)

