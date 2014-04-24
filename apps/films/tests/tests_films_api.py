#coding: utf-8

from django.db import transaction, IntegrityError

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apps.films.tests.factories_films_api import *
from apps.users.models.api_session import SessionToken, UsersApiSessions


class FilmsTest(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.genres = []
        self.locations = []
        self.contents = []
        self.films = []
        self.comments = []
        self.extras = []
        self.persons = []
        self.pfilms = []
        self.countries = []

        for i in range(4):
            self.genres.append(GenreFactory.create())
            self.countries.append(CountriesFactory.create())
        self.genres.append(GenreFactory.create())

        for i in range(2):
            for j in range(5):
                self.persons.append(PersonFactory.create())
            if i == 1:
                self.films.append(FilmFactory.create(
                    genres=(self.genres[2*i], self.genres[2*i+1], self.genres[4], self.genres[0]),
                    countries=(self.countries[2*i], self.countries[2*i+1]), type=APP_FILM_SERIAL
                ))
            else:
                self.films.append(FilmFactory.create(
                    genres=(self.genres[2*i], self.genres[2*i+1], self.genres[4]),
                    countries=(self.countries[2*i], self.countries[2*i+1])
                ))

            self.contents.append(ContentFactory.create(film=self.films[i]))
            self.locations.append(LocationFactory.create(content=self.contents[i]))
            for j in range(5):
                self.comments.append(CommentsFactory.create(content=self.contents[i], user=self.user))

            self.extras.append(FilmsExtrasFactory.create(film=self.films[i]))
            for j in range(5):
                if j % 2 is 0:
                    person_type = APP_PERSON_ACTOR
                else:
                    person_type = APP_PERSON_PRODUCER
                self.pfilms.append(PersonsFilmFactory.create(film=self.films[i], person=self.persons[j], p_type=person_type))

        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        self.headers = "%s %s" % ('X-VB-Token', s_token.key)

    def locations_assert(self, response_locations, locations):
        if len(response_locations) != len(locations):
            self.assertTrue(False)

        for i in range(len(response_locations)):
            self.assertEqual(response_locations[i]['id'], locations[i].id)
            self.assertEqual(response_locations[i]['type'], locations[i].type)
            self.assertEqual(response_locations[i]['lang'], locations[i].lang)
            self.assertEqual(response_locations[i]['quality'], locations[i].quality)
            self.assertEqual(response_locations[i]['subtitles'], locations[i].subtitles)
            self.assertEqual(response_locations[i]['price'], locations[i].price)
            self.assertEqual(response_locations[i]['price_type'], locations[i].price_type)
            self.assertEqual(response_locations[i]['url_view'], locations[i].url_view)

    def not_extend_assert(self, response_data, film, extras):
        self.assertEqual(response_data['poster'], extras.photo.url)
        self.assertEqual(response_data['id'], film.id)
        self.assertEqual(response_data['name'], film.name)
        self.assertEqual(response_data['name_orig'], film.name_orig)
        self.assertEqual(response_data['releasedate'], film.release_date)
        self.assertEqual(response_data['ratings']['kp'][0], film.rating_kinopoisk)
        self.assertEqual(response_data['ratings']['kp'][1], film.rating_kinopoisk_cnt)
        self.assertEqual(response_data['ratings']['imdb'][0], film.rating_imdb)
        self.assertEqual(response_data['ratings']['imdb'][1], film.rating_imdb_cnt)
        self.assertEqual(response_data['ratings']['cons'][0], 0)
        self.assertEqual(response_data['ratings']['cons'][1], 0)
        self.assertEqual(response_data['duration'], film.duration)
        self.assertEqual(response_data['relation'], {})

    def comment_assert(self, response_data, comments, film, start_count, data, user):
        self.assertEqual(response_data['page'], data['page'])
        self.assertEqual(response_data['per_page'], data['per_page'])
        self.assertEqual(response_data['total_cnt'], len(comments))
        for i in range(len(response_data['items'])):
            self.assertEqual(response_data['items'][i]['created'], comments[start_count+i].created)
            self.assertEqual(response_data['items'][i]['id'], comments[start_count+i].id)
            self.assertEqual(response_data['items'][i]['text'], comments[start_count+i].text)
            self.assertEqual(response_data['items'][i]['film'], {'id': film.id, 'name': film.name})
            self.assertEqual(response_data['items'][i]['user'], {'avatar': u'', 'id': user.id, 'user': user.profile.nickname})

    def extras_assert(self, response_data, extras):
        self.assertEqual(response_data['id'], extras.id)
        self.assertEqual(response_data['name'], extras.name)
        self.assertEqual(response_data['name_orig'], extras.name_orig)
        self.assertEqual(response_data['type'], extras.type)
        self.assertEqual(response_data['url'], extras.url)
        self.assertEqual(response_data['description'], extras.description)

    def extras_iter_assert(self, response_data, extras):
        if len(response_data) != len(extras):
            self.assertTrue(False)

        for i in range(len(response_data)):
            self.extras_assert(response_data[i], extras[i])

    def test_api_detail_ok_get(self):
        film = self.films[0]
        response = self.client.get(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_detail_data_get(self):
        film = self.films[0]
        locations = []
        extras = None
        for loc in self.locations:
            if film.id == loc.content.film.id:
                locations.append(loc)

        for ext in self.extras:
            if film.id == ext.film.id and len(ext.photo.url) is not 0:
                extras = ext
                break

        response = self.client.get(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.locations_assert(response.data['locations'], locations)
        self.not_extend_assert(response.data, film, extras)

    def test_api_detail_ok_post(self):
        film = self.films[0]
        response = self.client.post(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}), data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_detail_all_data_post(self):
        film = self.films[0]
        locations = []
        extras = None
        directors = []
        for persf in self.pfilms:
            if persf.film_id == film.id and persf.p_type == APP_PERSON_DIRECTOR:
                directors.append(persf.person)

        for loc in self.locations:
            if film.id == loc.content.film.id:
                locations.append(loc)

        for ext in self.extras:
            if film.id == ext.film.id and len(ext.photo.url) is not 0:
                extras = ext
                break

        response = self.client.post(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}), data={'extend': True, 'persons': True})
        if len(response.data['countries']) != len(film.countries.all().values('id', 'name')):
            self.assertTrue(False)
        if len(response.data['genres']) != len(film.genres.all().values('id', 'name')):
            self.assertTrue(False)
        if len(response.data['persons']) != len(film.persons.all().values('id', 'name', 'photo')):
            self.assertTrue(False)
        if len(response.data['directors']) != len(directors):
            self.assertTrue(False)
        for i in range(len(response.data['countries'])):
            self.assertEqual(response.data['countries'][i], film.countries.all().values('id', 'name')[i])
        for i in range(len(response.data['genres'])):
            self.assertEqual(response.data['genres'][i], film.genres.all().values('id', 'name')[i])
        for i in range(len(response.data['persons'])):
            self.assertEqual(response.data['persons'][i], film.persons.all().values('id', 'name', 'photo')[i])
        for i in range(len(response.data['directors'])):
            self.assertEqual(response.data['directors'][i], directors[i])
        self.locations_assert(response.data['locations'], locations)
        self.not_extend_assert(response.data, film, extras)
        self.assertEqual(response.data['description'], film.description)

    def test_api_detail_extend_data_post(self):
        film = self.films[0]
        locations = []
        directors = []
        for persf in self.pfilms:
            if persf.film_id == film.id and persf.p_type == APP_PERSON_DIRECTOR:
                directors.append(persf.person)

        for loc in self.locations:
            if film.id == loc.content.film.id:
                locations.append(loc)

        extras = None
        for ext in self.extras:
            if film.id == ext.film.id and len(ext.photo.url) is not 0:
                extras = ext
                break

        response = self.client.post(
            reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}),
            data={'extend': True, 'persons': False}
        )
        if len(response.data['directors']) != len(directors):
            self.assertTrue(False)
        if len(response.data['countries']) != len(film.countries.all().values('id', 'name')):
            self.assertTrue(False)

        if len(response.data['genres']) != len(film.genres.all().values('id', 'name')):
            self.assertTrue(False)

        for i in range(len(response.data['countries'])):
            self.assertEqual(response.data['countries'][i], film.countries.all().values('id', 'name')[i])

        for i in range(len(response.data['genres'])):
            self.assertEqual(response.data['genres'][i], film.genres.all().values('id', 'name')[i])

        for i in range(len(response.data['directors'])):
            self.assertEqual(response.data['directors'][i], directors[i])

        self.locations_assert(response.data['locations'], locations)
        self.not_extend_assert(response.data, film, extras)
        self.assertEqual(response.data['description'], film.description)

    def test_api_detail_persons_data_post(self):
        film = self.films[0]
        locations = []
        for loc in self.locations:
            if film.id == loc.content.film.id:
                locations.append(loc)

        extras = None
        for ext in self.extras:
            if film.id == ext.film.id and len(ext.photo.url) is not 0:
                extras = ext
                break

        response = self.client.post(
            reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}),
            data={'extend': False, 'persons': True}
        )
        self.locations_assert(response.data['locations'], locations)
        self.not_extend_assert(response.data, film, extras)

    def test_api_detail_data_without_param_post(self):
        film = self.films[0]
        locations = []
        for loc in self.locations:
            if film.id == loc.content.film.id:
                locations.append(loc)

        extras = None
        for ext in self.extras:
            if film.id == ext.film.id and len(ext.photo.url) is not 0:
                extras = ext
                break

        response = self.client.post(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}), data={})
        self.locations_assert(response.data['locations'], locations)
        self.not_extend_assert(response.data, film, extras)

    def test_api_detail_404_post(self):
        response = self.client.post(reverse('film_details_view', kwargs={'film_id': 0, 'format': 'json'}), data={})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_detail_404_get(self):
        response = self.client.get(reverse('film_details_view', kwargs={'film_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_action_comments_add_ok(self):
        film = self.films[0]
        data = {'text': u'Отличный фильм'}
        response = self.client.post(
            reverse('act_film_comment_view', kwargs={'film_id': film.id, 'format': 'json'}),
            HTTP_AUTHORIZATION=self.headers, data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment = Comments.objects.all().last()
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.content.film, film)
        self.assertEqual(comment.text, data['text'])

    def test_api_action_comments_add_bad(self):
        film = self.films[0]
        response = self.client.post(
            reverse('act_film_comment_view', kwargs={'film_id': film.id, 'format': 'json'}),
            HTTP_AUTHORIZATION=self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_action_comments_add_404(self):
        data = {'text': u'Отличный фильм'}
        response = self.client.post(reverse('act_film_comment_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_action_comments_add_not_authenticated(self):
        film = self.films[0]
        data = {'text': u'Отличный фильм'}
        response = self.client.post(reverse('act_film_comment_view', kwargs={'film_id': film.id, 'format': 'json'}), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_action_not_watch_add_new(self):
        film = self.films[0]
        response = self.client.get(reverse('act_film_notwatch_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_film = UsersFilms.objects.all().last()
        self.assertEqual(user_film.film, film)
        self.assertEqual(user_film.user, self.user)
        self.assertEqual(user_film.status, APP_USERFILM_STATUS_NOT_WATCH)

    def test_api_action_not_watch_update(self):
        film = self.films[0]
        with self.assertRaises(IntegrityError):
            response = self.client.get(reverse('act_film_notwatch_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            user_film = UsersFilms.objects.all().last()
            self.assertEqual(user_film.film, film)
            self.assertEqual(user_film.user, self.user)
            self.assertEqual(user_film.status, APP_USERFILM_STATUS_NOT_WATCH)
            with transaction.atomic():
                UsersFilmsFactory.create(user=self.user, film=film)

    def test_api_action_not_watch_not_authenticated(self):
        film = self.films[0]
        response = self.client.post(reverse('act_film_notwatch_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(reverse('act_film_notwatch_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_action_not_watch_delete_ok(self):
        film = self.films[0]
        UsersFilmsFactory.create(user=self.user, film=film, status=APP_USERFILM_STATUS_NOT_WATCH)
        response = self.client.delete(reverse('act_film_notwatch_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_film = UsersFilms.objects.all().last()
        self.assertEqual(user_film.film, film)
        self.assertEqual(user_film.user, self.user)
        self.assertEqual(user_film.status, APP_USERFILM_STATUS_UNDEF)

    def test_api_action_not_watch_delete_without_users_films_ok(self):
        film = self.films[0]
        response = self.client.delete(reverse('act_film_notwatch_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_action_not_watch_404(self):
        response = self.client.delete(reverse('act_film_notwatch_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(reverse('act_film_notwatch_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_action_playlist_add(self):
        film = self.films[0]
        response = self.client.get(reverse('act_film_playlist_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users_films = UsersFilms.objects.all().last()
        self.assertEqual(users_films.film, film)
        self.assertEqual(users_films.user, self.user)
        self.assertEqual(users_films.status, APP_USERFILM_STATUS_SUBS)
        self.assertEqual(users_films.subscribed, APP_USERFILM_SUBS_TRUE)

    def test_api_action_playlist_already_exist(self):
        film = self.films[0]
        UsersFilmsFactory.create(user=self.user, film=film, status=APP_USERFILM_STATUS_SUBS, subscribed=APP_USERFILM_SUBS_TRUE)
        response = self.client.get(reverse('act_film_playlist_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_action_playlist_404(self):
        response = self.client.get(reverse('act_film_playlist_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete(reverse('act_film_playlist_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_action_playlist_not_authenticated(self):
        film = self.films[0]
        response = self.client.delete(reverse('act_film_playlist_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(reverse('act_film_playlist_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_action_playlist_delete(self):
        film = self.films[0]
        UsersFilmsFactory.create(user=self.user, film=film, status=APP_USERFILM_STATUS_SUBS, subscribed=APP_USERFILM_SUBS_TRUE)
        response = self.client.delete(reverse('act_film_playlist_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertTrue(not UsersFilms.objects.all())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_action_playlist_add_serial(self):
        film = self.films[1]
        response = self.client.get(reverse('act_film_playlist_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users_films = UsersFilms.objects.all().last()
        self.assertEqual(users_films.film, film)
        self.assertEqual(users_films.user, self.user)
        self.assertEqual(users_films.status, APP_USERFILM_STATUS_SUBS)
        self.assertEqual(users_films.subscribed, APP_USERFILM_SUBS_FALSE)

    def test_api_action_rate_add(self):
        film = self.films[0]
        data = {'rating': 10}
        response = self.client.post(reverse('act_film_rate_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers, data=data)
        users_films = UsersFilms.objects.all().last()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(users_films.film, film)
        self.assertEqual(users_films.user, self.user)
        self.assertEqual(users_films.rating, data['rating'])

    def test_api_action_rate_update(self):
        film = self.films[0]
        data = {'rating': 10}
        with self.assertRaises(IntegrityError):
            response = self.client.post(reverse('act_film_rate_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers, data=data)
            users_films = UsersFilms.objects.all().last()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(users_films.film, film)
            self.assertEqual(users_films.user, self.user)
            self.assertEqual(users_films.rating, data['rating'])
            with transaction.atomic():
                UsersFilmsFactory.create(user=self.user, film=film)

    def test_api_action_rate_bad(self):
        film = self.films[0]
        response = self.client.post(reverse('act_film_rate_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_action_rate_not_authenticated(self):
        film = self.films[0]
        response = self.client.post(reverse('act_film_rate_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(reverse('act_film_rate_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_action_rate_delete(self):
        film = self.films[0]
        UsersFilmsFactory.create(user=self.user, film=film, rating=10)
        response = self.client.delete(reverse('act_film_rate_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users_films = UsersFilms.objects.all().last()
        self.assertEqual(users_films.film, film)
        self.assertEqual(users_films.user, self.user)
        self.assertEqual(users_films.rating, None)

    def test_api_action_rate_404(self):
        data = {'rating': 10}
        response = self.client.delete(reverse('act_film_rate_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.post(reverse('act_film_rate_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_action_subscribe_film(self):
        film = self.films[0]
        response = self.client.get(reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_action_subscribe_serial_add(self):
        film = self.films[1]
        response = self.client.get(reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users_films = UsersFilms.objects.all().last()
        self.assertEqual(users_films.film, film)
        self.assertEqual(users_films.user, self.user)
        self.assertEqual(users_films.subscribed, APP_USERFILM_SUBS_TRUE)

    def test_api_action_subscribe_serial_update(self):
        film = self.films[1]
        with self.assertRaises(IntegrityError):
            response = self.client.get(reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
            users_films = UsersFilms.objects.all().last()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(users_films.film, film)
            self.assertEqual(users_films.user, self.user)
            self.assertEqual(users_films.subscribed, APP_USERFILM_SUBS_TRUE)
            with transaction.atomic():
                UsersFilmsFactory.create(user=self.user, film=film)

    def test_api_action_subscribe_404(self):
        response = self.client.get(reverse('act_film_subscribe_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete(reverse('act_film_subscribe_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_action_subscribe_not_authenticated(self):
        film = self.films[1]
        response = self.client.get(reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_action_subscribe_delete_film(self):
        film = self.films[0]
        response = self.client.delete(
            reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}),
            HTTP_AUTHORIZATION=self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_action_subscribe_delete_serial(self):
        film = self.films[1]
        UsersFilmsFactory.create(user=self.user, film=film, subscribed=APP_USERFILM_SUBS_TRUE)

        response = self.client.delete(
            reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}),
            HTTP_AUTHORIZATION=self.headers
        )
        users_films = UsersFilms.objects.all().last()
        self.assertEqual(users_films.film, film)
        self.assertEqual(users_films.user, self.user)
        self.assertEqual(users_films.subscribed, APP_USERFILM_SUBS_FALSE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_similar(self):
        film = self.films[0]
        sim_film = self.films[1]
        locations = []
        extras = None
        for loc in self.locations:
            if sim_film.id == loc.content.film.id:
                locations.append(loc)
        for ext in self.extras:
            if sim_film.id == ext.film.id and len(ext.photo.url) is not 0:
                extras = ext
                break
        response = self.client.get(reverse('film_similar_view', kwargs={'film_id': film.id, 'format': 'json'}))
        if len(response.data) != 1:
            self.assertTrue(False)
        for film in response.data:
            self.locations_assert(film['locations'], locations)
            self.not_extend_assert(film, sim_film, extras)

    def test_api_similar_ok(self):
        film = self.films[0]
        response = self.client.get(reverse('film_similar_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_similar_404(self):
        response = self.client.get(reverse('film_similar_view', kwargs={'film_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_locations_ok(self):
        film = self.films[0]
        response = self.client.get(reverse('film_locations_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_locations_404(self):
        response = self.client.get(reverse('film_locations_view', kwargs={'film_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_locations_data(self):
        film = self.films[0]
        response = self.client.get(reverse('film_locations_view', kwargs={'film_id': film.id, 'format': 'json'}))
        locations = []
        for loc in self.locations:
            if film.id == loc.content.film.id:
                locations.append(loc)
        self.locations_assert(response.data, locations)

    def test_api_extras_ok(self):
        film = self.films[0]
        response = self.client.post(reverse('film_extras_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_extras_404(self):
        response = self.client.post(reverse('film_extras_view', kwargs={'film_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_extras_without_type_data(self):
        extras = []
        film = self.films[0]
        for ext in self.extras:
            if film.id == ext.film.id:
                extras.append(ext)

        response = self.client.post(reverse('film_extras_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.extras_iter_assert(response.data, extras)

    def test_api_extras_type_poster_data(self):
        extras = []
        film = self.films[0]
        data = {'type': APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER}
        for ext in self.extras:
            if film.id == ext.film.id:
                extras.append(ext)

        response = self.client.post(reverse('film_extras_view', kwargs={'film_id': film.id, 'format': 'json'}), data=data)
        self.extras_iter_assert(response.data, extras)

    def test_api_extras_type_trailer_data(self):
        film = self.films[0]
        data = {'type': APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER}
        response = self.client.post(reverse('film_extras_view', kwargs={'film_id': film.id, 'format': 'json'}), data=data)
        self.assertTrue(not response.data)

    def test_api_comments_ok(self):
        film = self.films[0]
        response = self.client.post(reverse('film_comments_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_comments_404(self):
        response = self.client.post(reverse('film_comments_view', kwargs={'film_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_comment_default_param(self):
        film = self.films[0]
        comments = []
        for comment in self.comments:
            if film.id == comment.content.film.id:
                comments.append(comment)

        data = {'page': 1, 'per_page': 10}
        response = self.client.post(reverse('film_comments_view', kwargs={'film_id': film.id, 'format': 'json'}))
        if len(comments) is not len(response.data['items']):
            self.assertTrue(False)

        self.comment_assert(response.data, comments, film, 0, data, self.user)

    def test_api_comment_with_param(self):
        comments = []
        film = self.films[0]
        for comment in self.comments:
            if film.id == comment.content.film.id:
                comments.append(comment)

        data = {'page': 2, 'per_page': 3}
        response = self.client.post(reverse('film_comments_view', kwargs={'film_id': film.id, 'format': 'json'}), data=data)
        self.comment_assert(response.data, comments, film, 3, data, self.user)

        data = {'page': 2, 'per_page': 2}
        response = self.client.post(reverse('film_comments_view', kwargs={'film_id': film.id, 'format': 'json'}), data=data)
        self.comment_assert(response.data, comments, film, 2, data, self.user)

    def test_api_persons_ok(self):
        film = self.films[0]
        response = self.client.get(reverse('film_persons_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_persons_404(self):
        response = self.client.get(reverse('film_persons_view', kwargs={'film_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_persons_default_param(self):
        film = self.films[0]
        response = self.client.get(reverse('film_persons_view', kwargs={'film_id': film.id, 'format': 'json'}))
        persons = []
        for persf in self.pfilms:
            if film.id == persf.film_id:
                persons.append(persf.person)
        if len(persons) != len(response.data):
            self.assertTrue(False)
        for i in range(len(response.data)):
            self.assertEqual(response.data[i]['id'], persons[i].id)
            self.assertEqual(response.data[i]['name'], persons[i].name)
            self.assertEqual(response.data[i]['photo'], persons[i].photo)

    def test_api_persons_with_user_param(self):
        film = self.films[0]
        data = {'type': APP_PERSON_ACTOR, 'top': 1, 'limit': 2}
        persons = []
        for persf in self.pfilms:
            if film.id == persf.film_id and persf.p_type == data['type']:
                persons.append(persf.person)
        response = self.client.get(reverse('film_persons_view', kwargs={'film_id': film.id, 'format': 'json'}), data=data)
        for i in range(len(response.data)):
            self.assertEqual(response.data[i]['id'], persons[data['top'] + i].id)
            self.assertEqual(response.data[i]['name'], persons[data['top'] + i].name)
            self.assertEqual(response.data[i]['photo'], persons[data['top'] + i].photo)

    def test_api_search_ok(self):
        data = {}
        response = self.client.get(reverse('film_search_view', kwargs={'format': 'json'}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_search_bad(self):
        data = {'video': 1, 'text': 2, 'page': 'hello'}
        response = self.client.get(reverse('film_search_view', kwargs={'format': 'json'}), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_search_text(self):
        film = self.films[0]
        locations = []
        for loc in self.locations:
            if film.id == loc.content.film.id:
                locations.append(loc)

        extras = None
        for ext in self.extras:
            if film.id == ext.film.id and len(ext.photo.url) is not 0:
                extras = ext
                break

        data = {'text': film.name}
        response = self.client.get(reverse('film_search_view', kwargs={'format': 'json'}), data=data)
        self.assertEqual(response.data['total_cnt'], 1)
        self.assertEqual(response.data['page'], 1)
        self.assertEqual(response.data['per_page'], 24)
        self.locations_assert(response.data['items'][0]['locations'], locations)
        self.not_extend_assert(response.data['items'][0], film, extras)

    def test_api_search_by_genre_and_others(self):
        film1 = self.films[0]
        film2 = self.films[1]
        locations1 = []
        locations2 = []
        for loc in self.locations:
            if film1.id == loc.content.film.id:
                locations1.append(loc)
            elif film2.id == loc.content.film.id:
                locations2.append(loc)

        extras1 = None
        extras2 = None
        for ext in self.extras:
            if film1.id == ext.film.id and len(ext.photo.url) is not 0:
                extras1 = ext
                break
        for ext in self.extras:
            if film2.id == ext.film.id and len(ext.photo.url) is not 0:
                extras2 = ext
                break

        data = {'genre': self.genres[4].id, 'year_old': 0, 'price': 100, 'instock': True, 'per_page': 2}
        response = self.client.get(reverse('film_search_view', kwargs={'format': 'json'}), data=data)
        self.assertEqual(response.data['total_cnt'], 2)
        self.assertEqual(response.data['page'], 1)
        self.assertEqual(response.data['per_page'], 2)
        self.locations_assert(response.data['items'][0]['locations'], locations1)
        self.not_extend_assert(response.data['items'][0], film1, extras1)
        self.locations_assert(response.data['items'][1]['locations'], locations2)
        self.not_extend_assert(response.data['items'][1], film2, extras2)
        data = {'genre': self.genres[4].id, 'year_old': 0, 'price': 100, 'instock': True, 'per_page': 1, 'page': 2}
        response = self.client.get(reverse('film_search_view', kwargs={'format': 'json'}), data=data)
        self.assertEqual(response.data['total_cnt'], 2)
        self.assertEqual(response.data['page'], 2)
        self.assertEqual(response.data['per_page'], 1)
        self.locations_assert(response.data['items'][0]['locations'], locations2)
        self.not_extend_assert(response.data['items'][0], film2, extras2)
