#coding: utf-8

from django.core.urlresolvers import reverse

from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from apps.films.models import UsersPersons

from apps.films.tests.factories import PersonsFilmFactory, PersonsExtrasFactory, UserFactory, FeedFactory
from apps.films.api.serializers import vbPerson
from apps.users import UsersApiSessions
from apps.users.models.api_session import SessionToken
from apps.users.models import Feed
from apps.users.constants import PERSON_SUBSCRIBE, PERSON_O


class PersonsTestCase(APITestCase):
    def setUp(self):
        self.person_filmography = PersonsFilmFactory.create()
        self.persons_extras = PersonsExtrasFactory.create()
        self.user = UserFactory.create()
        Token.objects.get(user=self.user)
        self.s_token = SessionToken.objects.create(user=self.user)

    def test_person_view_ok(self):
        response = self.client.get(reverse('person_api_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_person_view_404(self):
        response = self.client.get(reverse('person_api_view', kwargs={'resource_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_person_api_view_get(self):
        """В силу невозможности расширить PersonFactory нестандартными полями, несуществующими в модели,
        делаем сравнение с сериализованными полями vbPerson, т.к. такие поля возвращаются оттуда(по специф-и).
        """
        UsersApiSessions.objects.create(token=self.s_token)
        headers = self.s_token.key
        response = self.client.get(reverse('person_api_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}),
                                   HTTP_X_MI_SESSION=headers)
        self.assertEqual(response.data['id'], self.person_filmography.person.id)
        self.assertEqual(response.data['photo'], self.person_filmography.person.photo)
        self.assertEqual(response.data['name'], self.person_filmography.person.name)
        self.assertEqual(response.data['birthdate'], self.person_filmography.person.birthdate)
        vbdata = vbPerson(self.person_filmography.person, user=self.user).data
        self.assertEqual(response.data['relation'], vbdata['relation'])
        self.assertEqual(response.data['birthplace'], vbdata['birthplace'])

    def test_person_api_view_post(self):
        """В силу невозможности расширить PersonFactory нестандартными полями, несуществующими в модели,
        делаем сравнение с сериализованными полями vbPerson, т.к. такие поля возвращаются оттуда(по специф-и).
        """
        UsersApiSessions.objects.create(token=self.s_token)
        headers = self.s_token.key
        response = self.client.post(reverse('person_api_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}),
                                    data={'extend': True}, HTTP_X_MI_SESSION=headers)
        self.assertEqual(response.data['id'], self.person_filmography.person.id)
        self.assertEqual(response.data['photo'], self.person_filmography.person.photo)
        self.assertEqual(response.data['name'], self.person_filmography.person.name)
        self.assertEqual(response.data['birthdate'], self.person_filmography.person.birthdate)
        vbdata = vbPerson(self.person_filmography.person, user=self.user, extend=True).data
        self.assertEqual(response.data['relation'], vbdata['relation'])
        self.assertEqual(response.data['birthplace'], vbdata['birthplace'])
        self.assertEqual(response.data['bio'], vbdata['bio'])
        self.assertEqual(response.data['roles'], vbdata['roles'])

    def test_person_filmography_view_ok(self):
        response = self.client.get(reverse('person_filmography_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_person_filmography_view_404(self):
    #     response = self.client.get(reverse('person_filmography_view', kwargs={'resource_id': 0, 'format': 'json'}))
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_person_filmography_view(self):
        response = self.client.get(reverse('person_filmography_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}))
        for i in range(len(response.data['items'])):
            self.assertEqual(response.data['items'][i]['id'], self.person_filmography.film.id)
            self.assertEqual(response.data['items'][i]['name'], self.person_filmography.film.name)
            self.assertEqual(response.data['items'][i]['name_orig'], self.person_filmography.film.name_orig)
            self.assertEqual(response.data['items'][i]['releasedate'], self.person_filmography.film.release_date)

    def test_person_action_subscribe_api_view_ok(self):
        UsersApiSessions.objects.create(token=self.s_token)
        headers = self.s_token.key
        response = self.client.put(reverse('person_action_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}), HTTP_X_MI_SESSION=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_person_action_subscribe_api_view(self):
        UsersApiSessions.objects.create(token=self.s_token)
        headers = self.s_token.key
        response = self.client.put(reverse('person_action_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}), HTTP_X_MI_SESSION=headers)
        user_person = UsersPersons.objects.all().last()
        feed = Feed.objects.last()
        self.assertEqual(feed.user, self.user)
        self.assertEqual(feed.type, PERSON_SUBSCRIBE)
        self.assertEqual(feed.obj_id, self.person_filmography.person.id)
        self.assertEqual(user_person.person, self.person_filmography.person)
        self.assertEqual(user_person.user, self.user)
        self.assertEqual(user_person.subscribed, 1)

    def test_person_action_subscribe_update_api_view(self):
        UsersApiSessions.objects.create(token=self.s_token)
        headers = self.s_token.key
        FeedFactory.create(user=self.user, type=PERSON_SUBSCRIBE, obj_id=self.person_filmography.person.id)
        response = self.client.put(reverse('person_action_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}), HTTP_X_MI_SESSION=headers)
        user_person = UsersPersons.objects.all().last()
        feed = Feed.objects.last()
        self.assertEqual(feed.user, self.user)
        self.assertEqual(feed.type, PERSON_SUBSCRIBE)
        self.assertEqual(feed.obj_id, self.person_filmography.person.id)
        self.assertEqual(user_person.person, self.person_filmography.person)
        self.assertEqual(user_person.user, self.user)
        self.assertEqual(user_person.subscribed, 1)

    def test_person_action_subscribe_delete(self):
        UsersApiSessions.objects.create(token=self.s_token)
        headers = self.s_token.key
        self.client.put(reverse('person_action_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}), HTTP_X_MI_SESSION=headers)
        self.assertTrue(Feed.objects.all().exists())
        self.client.delete(reverse('person_action_view', kwargs={'resource_id': self.person_filmography.person.id, 'format': 'json'}), HTTP_X_MI_SESSION=headers)
        user_person = UsersPersons.objects.last()
        self.assertFalse(Feed.objects.all().exists())
        self.assertEqual(user_person.subscribed, 0)
        self.assertEqual(user_person.person, self.person_filmography.person)
        self.assertEqual(user_person.user, self.user)

    def test_person_extras_view_ok(self):
        response = self.client.get(reverse('person_extras_view', kwargs={'resource_id': self.persons_extras.person.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_person_extras_view_404(self):
        response = self.client.get(reverse('person_extras_view', kwargs={'resource_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_person_extras_view(self):
        response = self.client.get(reverse('person_extras_view', kwargs={'resource_id': self.persons_extras.person.id, 'format': 'json'}))
        self.assertEqual(response.data[0]['name'], self.persons_extras.name)
        self.assertEqual(response.data[0]['name_orig'], self.persons_extras.name_orig)
        self.assertEqual(response.data[0]['description'], self.persons_extras.description)
