#coding: utf-8
from apps.films.api import DetailFilmView
from apps.films.api.serializers import vbFilm

__author__ = 'ipatov'
from apps.films.tests.factories import ContentFactory, FilmFactory, LocationFactory
from apps.films.views import PersonAPIView
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.reverse import reverse
import json


class FilmsTest(APITestCase):
    """
    Метод  post не тестируем, т.к. там те же действия что и в get
    """
    def setUp(self):
        self.location = LocationFactory.create()

    def test_api_detail_ok(self):
        response = self.client.get(reverse('film_details_view', kwargs={'film_id': self.content.film.id, 'format': 'json'}))
        print response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_detail_data(self):
        response = self.client.get(reverse('film_details_view', kwargs={'film_id': self.content.film.id, 'format': 'json'}))
        print response.data['content']['film'].__dict__
        self.assertEqual(response.data['id'], self.film.id)
        self.assertEqual(response.data['name'], self.film.name)
        self.assertEqual(response.data['name_orig'], self.film.name_orig)
        self.assertEqual(response.data['release_date'], self.film.release_date)
        self.assertEqual(response.data['description'], self.film.description)
        self.assertEqual(response.data['ratings']['kp'][0], self.film.rating_kinopoisk)
        self.assertEqual(response.data['ratings']['kp'][1], self.film.rating_kinopoisk_cnt)
        self.assertEqual(response.data['ratings']['imdb'][0], self.film.rating_imdb)
        self.assertEqual(response.data['ratings']['imdb'][1], self.film.rating_imdb_cnt)
        self.assertEqual(response.data['ratings']['cons'][0], 0)
        self.assertEqual(response.data['ratings']['cons'][1], 0)
        self.assertEqual(response.data['duration'], self.film.duration)
        self.assertEqual(response.data['poster'], [])
        self.assertEqual(response.data['countries'], [])
        self.assertEqual(response.data['genres'], [])
        self.assertEqual(response.data['persons'], [])
        self.assertEqual(response.data['locations'], [])
        self.assertEqual(response.data['relation'], [])

    def test_api_detail_404(self):
        response = self.client.get(reverse('film_details_view', kwargs={'film_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_search(self):
        data = {'text': u'RED5'}
        response = self.client.post(reverse('film_search_view', kwargs={'format': 'json'}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
