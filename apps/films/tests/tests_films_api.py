#coding: utf-8
from apps.films.api import DetailFilmView
from apps.films.api.serializers import vbFilm

__author__ = 'ipatov'
from apps.films.tests.factories import ContentFactory, FilmFactory, LocationFactory, GenreFactory
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
    Метод  post в film_datail не тестируем, т.к. там те же действия что и в get
    """
    def setUp(self):
        self.genres = []
        self.locations = []
        self.films = []
        for i in range(4):
            self.genres.append(GenreFactory.create())
        for i in range(2):
            self.locations.append(LocationFactory.create(content__film__genres=(self.genres[2*i], self.genres[2*i+1])))
        for location in self.locations:
            self.films.append(location.content.film)

    def test_api_detail_ok(self):
        film = self.films[0]
        response = self.client.get(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_detail_data(self):
        film = self.films[0]
        location = None
        for loc in self.locations:
            if film.id == loc.content.film.id:
                location = loc
                break
        response = self.client.get(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.data['id'], film.id)
        self.assertEqual(response.data['name'], film.name)
        self.assertEqual(response.data['name_orig'], film.name_orig)
        self.assertEqual(response.data['release_date'], film.release_date)
        self.assertEqual(response.data['description'], film.description)
        self.assertEqual(response.data['ratings']['kp'][0], film.rating_kinopoisk)
        self.assertEqual(response.data['ratings']['kp'][1], film.rating_kinopoisk_cnt)
        self.assertEqual(response.data['ratings']['imdb'][0], film.rating_imdb)
        self.assertEqual(response.data['ratings']['imdb'][1], film.rating_imdb_cnt)
        self.assertEqual(response.data['ratings']['cons'][0], 0)
        self.assertEqual(response.data['ratings']['cons'][1], 0)
        self.assertEqual(response.data['duration'], film.duration)
        self.assertEqual(response.data['poster'], [])
        self.assertEqual(response.data['countries'], [])
        self.assertEqual(response.data['genres'][0], film.genres.all().values('id', 'name')[0])
        self.assertEqual(response.data['persons'], [])
        self.assertEqual(response.data['locations']['id'], location.id)
        self.assertEqual(response.data['locations']['content'], location.content.id)
        self.assertEqual(response.data['locations']['type'], location.type)
        self.assertEqual(response.data['locations']['lang'], location.lang)
        self.assertEqual(response.data['locations']['quality'], location.quality)
        self.assertEqual(response.data['locations']['subtitles'], location.subtitles)
        self.assertEqual(response.data['locations']['price'], location.price)
        self.assertEqual(response.data['locations']['price_type'], location.price_type)
        self.assertEqual(response.data['locations']['url_view'], location.url_view)
        self.assertEqual(response.data['relation'], [])

    def test_api_detail_404(self):
        response = self.client.get(reverse('film_details_view', kwargs={'film_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_search(self):
        film = self.films[0]
        data = {'text': film.name}
        response = self.client.post(reverse('film_search_view', kwargs={'format': 'json'}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
