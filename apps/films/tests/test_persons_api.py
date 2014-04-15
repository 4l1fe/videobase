from apps.films.tests.factories import PersonFactory, FilmFactory, PersonsFilmography
from apps.films.views import PersonAPIView
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class PersonsTest(APITestCase):
    def setUp(self):
        self.person = PersonFactory.create()
        #self.film = FilmFactory.create()
        #self.person_filmography = PersonsFilmography.create()

    def test_person_view_ok(self):
        response = self.client.get(reverse('person_api_view', kwargs={'resource_id': self.person.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_person_view_404(self):
        response = self.client.get(reverse('person_api_view', kwargs={'resource_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_person_api_view(self):
        response = self.client.get(reverse('person_api_view', kwargs={'resource_id': self.person.id, 'format': 'json'}))
        self.assertEqual(response.data['id'], self.person.id)
        self.assertEqual(response.data['photo'], self.person.photo)
        self.assertEqual(response.data['name'], self.person.name)

    def test_person_filmography_view_ok(self):
        response = self.client.get(reverse('person_filmography_view', kwargs={'resource_id': self.person.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_person_filmography_view_404(self):
        response = self.client.get(reverse('person_filmography_view', kwargs={'resource_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_person_filmography_view(self):
        response = self.client.get(reverse('person_filmography_view', kwargs={'resource_id': self.person.id, 'format': 'json'}))
        print response.data






