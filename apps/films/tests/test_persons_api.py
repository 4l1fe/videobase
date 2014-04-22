#coding: utf-8
from apps.films.tests.factories import *
from apps.users import UsersApiSessions
from apps.users.models.api_session import SessionToken
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class PersonsTest(APITestCase):
    def setUp(self):
        self.person_filmography = PersonsFilmography.create()
        self.persons_extras_factory = PersonsExtrasFactory.create()
        self.content_factory = ContentFactory.create()
        self.user_factory = UserFactory.create()
        Token.objects.get(user=self.user_factory)
        self.s_token = SessionToken.objects.create(user=self.user_factory)


    def test_person_view_ok(self):
        response = self.client.get(reverse('person_api_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_person_view_404(self):
        response = self.client.get(reverse('person_api_view', kwargs={'resource_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_person_api_view(self):
        response = self.client.get(reverse('person_api_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}))
        self.assertEqual(response.data['id'], self.person_filmography.person.id)
        self.assertEqual(response.data['photo'], self.person_filmography.person.photo)
        self.assertEqual(response.data['name'], self.person_filmography.person.name)

    def test_person_filmography_view_ok(self):
        response = self.client.get(reverse('person_filmography_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_person_filmography_view_404(self):
        response = self.client.get(reverse('person_filmography_view', kwargs={'resource_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_person_filmography_view(self):
        response = self.client.get(reverse('person_filmography_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}))
        self.assertEqual(response.data[0]['id'], self.person_filmography.film.id)
        self.assertEqual(response.data[0]['name'], self.person_filmography.film.name)
        self.assertEqual(response.data[0]['name_orig'], self.person_filmography.film.name_orig)
        self.assertEqual(response.data[0]['release_date'], self.person_filmography.film.release_date)

    def test_person_action_subscribe_api_view_ok(self):
        pass

    def test_person_action_subscribe_api_view(self):
        UsersApiSessions.objects.create(token=self.s_token)
        headers = "%s %s" % ('X-VB-Token', self.s_token.key)
        self.client.post(reverse('person_action_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        user_person = UsersPersons.objects.all().last()
        self.assertEqual(user_person.person, self.person_filmography.person)
        self.assertEqual(user_person.user, self.user_factory)
        self.assertEqual(user_person.subscribed, 1)


    def test_person_action_subscribe_delete(self):
        UsersApiSessions.objects.create(token=self.s_token)
        headers = "%s %s" % ('X-VB-Token', self.s_token.key)
        self.client.post(reverse('person_action_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.client.delete(reverse('person_action_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        user_person = UsersPersons.objects.last()
        self.assertEqual(user_person.subscribed, 0)
        self.assertEqual(user_person.person, self.person_filmography.person)
        self.assertEqual(user_person.user, self.user_factory)

    def test_person_extras_view_ok(self):
        response = self.client.get(reverse('person_extras_view', kwargs={'resource_id': self.persons_extras_factory.person.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_person_extras_view_404(self):
        response = self.client.get(reverse('person_extras_view', kwargs={'resource_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_person_extras_view(self):
        response = self.client.get(reverse('person_extras_view', kwargs={'resource_id': self.persons_extras_factory.person.id, 'format': 'json'}))
        self.assertEqual(response.data[0]['name'], self.persons_extras_factory.name)
        self.assertEqual(response.data[0]['name_orig'], self.persons_extras_factory.name_orig)
        self.assertEqual(response.data[0]['description'], self.persons_extras_factory.description)





