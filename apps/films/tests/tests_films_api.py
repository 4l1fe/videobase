#coding: utf-8

from django.db import transaction, IntegrityError

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apps.films.tests.factories_films_api import *
from apps.users.models.api_session import SessionToken, UsersApiSessions
# from apps.films.tests.factories_films_api import *
# from apps.users.models.api_session import SessionToken, UsersApiSessions


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
            self.persons.append(PersonFactory.create())
            if i == 1:
                self.films.append(FilmFactory.create(genres=(self.genres[2*i], self.genres[2*i+1], self.genres[4], self.genres[0]), countries=(self.countries[2*i], self.countries[2*i+1]), type=APP_FILM_SERIAL))
            else:
                self.films.append(FilmFactory.create(genres=(self.genres[2*i], self.genres[2*i+1], self.genres[4]), countries=(self.countries[2*i], self.countries[2*i+1])))
            self.contents.append(ContentFactory.create(film=self.films[i]))
            self.locations.append(LocationFactory.create(content=self.contents[i]))
            self.comments.append(CommentsFactory.create(content=self.contents[i], user=self.user))
            self.extras.append(FilmsExtrasFactory.create(film=self.films[i]))
            self.pfilms.append(PersonsFilmFactory.create(film=self.films[i], person=self.persons[i]))

    def test_api_detail_ok_get(self):
        film = self.films[0]
        response = self.client.get(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_detail_data_get(self):
        film = self.films[0]
        locations = []
        extras = []
        for loc in self.locations:
            if film.id == loc.content.film.id:
                locations.append(loc)
        for ext in self.extras:
            if film.id == ext.film.id:
                extras.append(ext)

        response = self.client.get(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}))
        if len(response.data['locations']) != len(locations):
            self.assertTrue(False)
        for i in range(len(response.data['locations'])):
            self.assertEqual(response.data['locations'][i]['id'], locations[i].id)
            self.assertEqual(response.data['locations'][i]['type'], locations[i].type)
            self.assertEqual(response.data['locations'][i]['lang'], locations[i].lang)
            self.assertEqual(response.data['locations'][i]['quality'], locations[i].quality)
            self.assertEqual(response.data['locations'][i]['subtitles'], locations[i].subtitles)
            self.assertEqual(response.data['locations'][i]['price'], locations[i].price)
            self.assertEqual(response.data['locations'][i]['price_type'], locations[i].price_type)
            self.assertEqual(response.data['locations'][i]['url_view'], locations[i].url_view)
        if len(response.data['poster']) != len(extras):
            self.assertTrue(False)
        for i in range(len(response.data['poster'])):
            self.assertEqual(response.data['poster'][i], extras[i].url)
        self.assertEqual(response.data['id'], film.id)
        self.assertEqual(response.data['name'], film.name)
        self.assertEqual(response.data['name_orig'], film.name_orig)
        self.assertEqual(response.data['release_date'], film.release_date)
        self.assertEqual(response.data['ratings']['kp'][0], film.rating_kinopoisk)
        self.assertEqual(response.data['ratings']['kp'][1], film.rating_kinopoisk_cnt)
        self.assertEqual(response.data['ratings']['imdb'][0], film.rating_imdb)
        self.assertEqual(response.data['ratings']['imdb'][1], film.rating_imdb_cnt)
        self.assertEqual(response.data['ratings']['cons'][0], 0)
        self.assertEqual(response.data['ratings']['cons'][1], 0)
        self.assertEqual(response.data['duration'], film.duration)
        self.assertEqual(response.data['relation'], [])

    def test_api_detail_ok_post(self):
        film = self.films[0]
        response = self.client.post(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}), data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_detail_all_data_post(self):
        film = self.films[0]
        locations = []
        extras = []
        for loc in self.locations:
            if film.id == loc.content.film.id:
                locations.append(loc)
        for ext in self.extras:
            if film.id == ext.film.id:
                extras.append(ext)
        response = self.client.post(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}), data={'extend': True, 'persons': True})
        if len(response.data['countries']) != len(film.countries.all().values('id', 'name')):
            self.assertTrue(False)
        if len(response.data['genres']) != len(film.genres.all().values('id', 'name')):
            self.assertTrue(False)
        if len(response.data['persons']) != len(film.persons.all().values('id', 'name', 'photo')):
            self.assertTrue(False)
        for i in range(len(response.data['countries'])):
            self.assertEqual(response.data['countries'][i], film.countries.all().values('id', 'name')[i])
        for i in range(len(response.data['genres'])):
            self.assertEqual(response.data['genres'][i], film.genres.all().values('id', 'name')[i])
        for i in range(len(response.data['persons'])):
            self.assertEqual(response.data['persons'][i], film.persons.all().values('id', 'name', 'photo')[i])
        if len(response.data['locations']) != len(locations):
            self.assertTrue(False)
        for i in range(len(response.data['locations'])):
            self.assertEqual(response.data['locations'][i]['id'], locations[i].id)
            self.assertEqual(response.data['locations'][i]['type'], locations[i].type)
            self.assertEqual(response.data['locations'][i]['lang'], locations[i].lang)
            self.assertEqual(response.data['locations'][i]['quality'], locations[i].quality)
            self.assertEqual(response.data['locations'][i]['subtitles'], locations[i].subtitles)
            self.assertEqual(response.data['locations'][i]['price'], locations[i].price)
            self.assertEqual(response.data['locations'][i]['price_type'], locations[i].price_type)
            self.assertEqual(response.data['locations'][i]['url_view'], locations[i].url_view)
        if len(response.data['poster']) != len(extras):
            self.assertTrue(False)
        for i in range(len(response.data['poster'])):
            self.assertEqual(response.data['poster'][i], extras[i].url)
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
        self.assertEqual(response.data['relation'], [])

    def test_api_detail_extend_data_post(self):
        film = self.films[0]
        locations = []
        extras = []
        for loc in self.locations:
            if film.id == loc.content.film.id:
                locations.append(loc)
        for ext in self.extras:
            if film.id == ext.film.id:
                extras.append(ext)
        response = self.client.post(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}), data={'extend': True, 'persons': False})
        if len(response.data['countries']) != len(film.countries.all().values('id', 'name')):
            self.assertTrue(False)
        if len(response.data['genres']) != len(film.genres.all().values('id', 'name')):
            self.assertTrue(False)
        for i in range(len(response.data['countries'])):
            self.assertEqual(response.data['countries'][i], film.countries.all().values('id', 'name')[i])
        for i in range(len(response.data['genres'])):
            self.assertEqual(response.data['genres'][i], film.genres.all().values('id', 'name')[i])
        if len(response.data['locations']) != len(locations):
            self.assertTrue(False)
        for i in range(len(response.data['locations'])):
            self.assertEqual(response.data['locations'][i]['id'], locations[i].id)
            self.assertEqual(response.data['locations'][i]['type'], locations[i].type)
            self.assertEqual(response.data['locations'][i]['lang'], locations[i].lang)
            self.assertEqual(response.data['locations'][i]['quality'], locations[i].quality)
            self.assertEqual(response.data['locations'][i]['subtitles'], locations[i].subtitles)
            self.assertEqual(response.data['locations'][i]['price'], locations[i].price)
            self.assertEqual(response.data['locations'][i]['price_type'], locations[i].price_type)
            self.assertEqual(response.data['locations'][i]['url_view'], locations[i].url_view)
        if len(response.data['poster']) != len(extras):
            self.assertTrue(False)
        for i in range(len(response.data['poster'])):
            self.assertEqual(response.data['poster'][i], extras[i].url)
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
        self.assertEqual(response.data['relation'], [])

    def test_api_detail_persons_data_post(self):
        film = self.films[0]
        locations = []
        extras = []
        for loc in self.locations:
            if film.id == loc.content.film.id:
                locations.append(loc)
        for ext in self.extras:
            if film.id == ext.film.id:
                extras.append(ext)
        response = self.client.post(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}), data={'extend': False, 'persons': True})
        if len(response.data['locations']) != len(locations):
            self.assertTrue(False)
        for i in range(len(response.data['locations'])):
            self.assertEqual(response.data['locations'][i]['id'], locations[i].id)
            self.assertEqual(response.data['locations'][i]['type'], locations[i].type)
            self.assertEqual(response.data['locations'][i]['lang'], locations[i].lang)
            self.assertEqual(response.data['locations'][i]['quality'], locations[i].quality)
            self.assertEqual(response.data['locations'][i]['subtitles'], locations[i].subtitles)
            self.assertEqual(response.data['locations'][i]['price'], locations[i].price)
            self.assertEqual(response.data['locations'][i]['price_type'], locations[i].price_type)
            self.assertEqual(response.data['locations'][i]['url_view'], locations[i].url_view)
        if len(response.data['poster']) != len(extras):
            self.assertTrue(False)
        for i in range(len(response.data['poster'])):
            self.assertEqual(response.data['poster'][i], extras[i].url)
        self.assertEqual(response.data['id'], film.id)
        self.assertEqual(response.data['name'], film.name)
        self.assertEqual(response.data['name_orig'], film.name_orig)
        self.assertEqual(response.data['release_date'], film.release_date)
        self.assertEqual(response.data['ratings']['kp'][0], film.rating_kinopoisk)
        self.assertEqual(response.data['ratings']['kp'][1], film.rating_kinopoisk_cnt)
        self.assertEqual(response.data['ratings']['imdb'][0], film.rating_imdb)
        self.assertEqual(response.data['ratings']['imdb'][1], film.rating_imdb_cnt)
        self.assertEqual(response.data['ratings']['cons'][0], 0)
        self.assertEqual(response.data['ratings']['cons'][1], 0)
        self.assertEqual(response.data['duration'], film.duration)
        self.assertEqual(response.data['relation'], [])

    def test_api_detail_data_without_param_post(self):
        film = self.films[0]
        locations = []
        extras = []
        for loc in self.locations:
            if film.id == loc.content.film.id:
                locations.append(loc)
        for ext in self.extras:
            if film.id == ext.film.id:
                extras.append(ext)
        response = self.client.post(reverse('film_details_view', kwargs={'film_id': film.id, 'format': 'json'}), data={})
        if len(response.data['locations']) != len(locations):
            self.assertTrue(False)
        for i in range(len(response.data['locations'])):
            self.assertEqual(response.data['locations'][i]['id'], locations[i].id)
            self.assertEqual(response.data['locations'][i]['type'], locations[i].type)
            self.assertEqual(response.data['locations'][i]['lang'], locations[i].lang)
            self.assertEqual(response.data['locations'][i]['quality'], locations[i].quality)
            self.assertEqual(response.data['locations'][i]['subtitles'], locations[i].subtitles)
            self.assertEqual(response.data['locations'][i]['price'], locations[i].price)
            self.assertEqual(response.data['locations'][i]['price_type'], locations[i].price_type)
            self.assertEqual(response.data['locations'][i]['url_view'], locations[i].url_view)
        if len(response.data['poster']) != len(extras):
            self.assertTrue(False)
        for i in range(len(response.data['poster'])):
            self.assertEqual(response.data['poster'][i], extras[i].url)
        self.assertEqual(response.data['id'], film.id)
        self.assertEqual(response.data['name'], film.name)
        self.assertEqual(response.data['name_orig'], film.name_orig)
        self.assertEqual(response.data['release_date'], film.release_date)
        self.assertEqual(response.data['ratings']['kp'][0], film.rating_kinopoisk)
        self.assertEqual(response.data['ratings']['kp'][1], film.rating_kinopoisk_cnt)
        self.assertEqual(response.data['ratings']['imdb'][0], film.rating_imdb)
        self.assertEqual(response.data['ratings']['imdb'][1], film.rating_imdb_cnt)
        self.assertEqual(response.data['ratings']['cons'][0], 0)
        self.assertEqual(response.data['ratings']['cons'][1], 0)
        self.assertEqual(response.data['duration'], film.duration)
        self.assertEqual(response.data['relation'], [])

    def test_api_detail_404_post(self):
        response = self.client.post(reverse('film_details_view', kwargs={'film_id': 0, 'format': 'json'}), data={})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_detail_404_get(self):
        response = self.client.get(reverse('film_details_view', kwargs={'film_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_search(self):
        film = self.films[0]
        data = {'text': film.name}
        response = self.client.get(reverse('film_search_view', kwargs={'format': 'json'}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_action_comments_add_ok(self):
        film = self.films[0]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        data = {'text': u'Отличный фильм'}
        response = self.client.post(reverse('act_film_comment_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment = Comments.objects.all().last()
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.content.film, film)
        self.assertEqual(comment.text, data['text'])

    def test_api_action_comments_add_bad(self):
        film = self.films[0]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.post(reverse('act_film_comment_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_action_comments_add_404(self):
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        data = {'text': u'Отличный фильм'}
        response = self.client.post(reverse('act_film_comment_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=headers, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_action_comments_add_not_authenticated(self):
        film = self.films[0]
        data = {'text': u'Отличный фильм'}
        response = self.client.post(reverse('act_film_comment_view', kwargs={'film_id': film.id, 'format': 'json'}), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_action_not_watch_add_new(self):
        film = self.films[0]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.get(reverse('act_film_notwatch_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_film = UsersFilms.objects.all().last()
        self.assertEqual(user_film.film, film)
        self.assertEqual(user_film.user, self.user)
        self.assertEqual(user_film.status, APP_USERFILM_STATUS_NOT_WATCH)

    def test_api_action_not_watch_update(self):
        film = self.films[0]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        with self.assertRaises(IntegrityError):
            response = self.client.get(reverse('act_film_notwatch_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
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
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.delete(reverse('act_film_notwatch_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_film = UsersFilms.objects.all().last()
        self.assertEqual(user_film.film, film)
        self.assertEqual(user_film.user, self.user)
        self.assertEqual(user_film.status, APP_USERFILM_STATUS_UNDEF)

    def test_api_action_not_watch_delete_without_users_films_ok(self):
        film = self.films[0]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.delete(reverse('act_film_notwatch_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_action_not_watch_404(self):
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.delete(reverse('act_film_notwatch_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(reverse('act_film_notwatch_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_action_playlist_add(self):
        film = self.films[0]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.get(reverse('act_film_playlist_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users_films = UsersFilms.objects.all().last()
        self.assertEqual(users_films.film, film)
        self.assertEqual(users_films.user, self.user)
        self.assertEqual(users_films.status, APP_USERFILM_STATUS_SUBS)
        self.assertEqual(users_films.subscribed, APP_USERFILM_SUBS_TRUE)

    def test_api_action_playlist_already_exist(self):
        film = self.films[0]
        UsersFilmsFactory.create(user=self.user, film=film, status=APP_USERFILM_STATUS_SUBS, subscribed=APP_USERFILM_SUBS_TRUE)
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.get(reverse('act_film_playlist_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_action_playlist_404(self):
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.get(reverse('act_film_playlist_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete(reverse('act_film_playlist_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
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
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.delete(reverse('act_film_playlist_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertTrue(not UsersFilms.objects.all())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_action_playlist_add_serial(self):
        film = self.films[1]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.get(reverse('act_film_playlist_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users_films = UsersFilms.objects.all().last()
        self.assertEqual(users_films.film, film)
        self.assertEqual(users_films.user, self.user)
        self.assertEqual(users_films.status, APP_USERFILM_STATUS_SUBS)
        self.assertEqual(users_films.subscribed, APP_USERFILM_SUBS_FALSE)

    def test_api_action_rate_add(self):
        film = self.films[0]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        data = {'rating': 10}
        response = self.client.post(reverse('act_film_rate_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers, data=data)
        users_films = UsersFilms.objects.all().last()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(users_films.film, film)
        self.assertEqual(users_films.user, self.user)
        self.assertEqual(users_films.rating, data['rating'])

    def test_api_action_rate_update(self):
        film = self.films[0]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        data = {'rating': 10}
        with self.assertRaises(IntegrityError):
            response = self.client.post(reverse('act_film_rate_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers, data=data)
            users_films = UsersFilms.objects.all().last()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(users_films.film, film)
            self.assertEqual(users_films.user, self.user)
            self.assertEqual(users_films.rating, data['rating'])
            with transaction.atomic():
                UsersFilmsFactory.create(user=self.user, film=film)

    def test_api_action_rate_bad(self):
        film = self.films[0]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.post(reverse('act_film_rate_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_action_rate_not_authenticated(self):
        film = self.films[0]
        response = self.client.post(reverse('act_film_rate_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(reverse('act_film_rate_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_action_rate_delete(self):
        film = self.films[0]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        UsersFilmsFactory.create(user=self.user, film=film, rating=10)
        response = self.client.delete(reverse('act_film_rate_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users_films = UsersFilms.objects.all().last()
        self.assertEqual(users_films.film, film)
        self.assertEqual(users_films.user, self.user)
        self.assertEqual(users_films.rating, None)

    def test_api_action_rate_404(self):
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        data = {'rating': 10}
        response = self.client.delete(reverse('act_film_rate_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.post(reverse('act_film_rate_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=headers, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_action_subscribe_film(self):
        film = self.films[0]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.get(reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_action_subscribe_serial_add(self):
        film = self.films[1]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.get(reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users_films = UsersFilms.objects.all().last()
        self.assertEqual(users_films.film, film)
        self.assertEqual(users_films.user, self.user)
        self.assertEqual(users_films.subscribed, APP_USERFILM_SUBS_TRUE)

    def test_api_action_subscribe_serial_update(self):
        film = self.films[1]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        with self.assertRaises(IntegrityError):
            response = self.client.get(reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
            users_films = UsersFilms.objects.all().last()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(users_films.film, film)
            self.assertEqual(users_films.user, self.user)
            self.assertEqual(users_films.subscribed, APP_USERFILM_SUBS_TRUE)
            with transaction.atomic():
                UsersFilmsFactory.create(user=self.user, film=film)

    def test_api_action_subscribe_404(self):
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.get(reverse('act_film_subscribe_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete(reverse('act_film_subscribe_view', kwargs={'film_id': 0, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_action_subscribe_not_authenticated(self):
        film = self.films[1]
        response = self.client.get(reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_action_subscribe_delete_film(self):
        film = self.films[0]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.delete(reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_action_subscribe_delete_serial(self):
        film = self.films[1]
        UsersFilmsFactory.create(user=self.user, film=film, subscribed=APP_USERFILM_SUBS_TRUE)
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.delete(reverse('act_film_subscribe_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers)
        users_films = UsersFilms.objects.all().last()
        self.assertEqual(users_films.film, film)
        self.assertEqual(users_films.user, self.user)
        self.assertEqual(users_films.subscribed, APP_USERFILM_SUBS_FALSE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_similar(self):
        film = self.films[0]
        sim_film = self.films[1]
        locations = []
        extras = []
        for loc in self.locations:
            if sim_film.id == loc.content.film.id:
                locations.append(loc)
        for ext in self.extras:
            if sim_film.id == ext.film.id:
                extras.append(ext)
        response = self.client.get(reverse('film_similar_view', kwargs={'film_id': film.id, 'format': 'json'}))
        if len(response.data) != 1:
            self.assertTrue(False)
        for film in response.data:
            if len(film['locations']) != len(locations):
                self.assertTrue(False)
            for i in range(len(film['locations'])):
                self.assertEqual(film['locations'][i]['id'], locations[i].id)
                self.assertEqual(film['locations'][i]['type'], locations[i].type)
                self.assertEqual(film['locations'][i]['lang'], locations[i].lang)
                self.assertEqual(film['locations'][i]['quality'], locations[i].quality)
                self.assertEqual(film['locations'][i]['subtitles'], locations[i].subtitles)
                self.assertEqual(film['locations'][i]['price'], locations[i].price)
                self.assertEqual(film['locations'][i]['price_type'], locations[i].price_type)
                self.assertEqual(film['locations'][i]['url_view'], locations[i].url_view)
            if len(film['poster']) != len(extras):
                self.assertTrue(False)
            for i in range(len(film['poster'])):
                self.assertEqual(film['poster'][i], extras[i].url)
            self.assertEqual(film['id'], sim_film.id)
            self.assertEqual(film['name'], sim_film.name)
            self.assertEqual(film['name_orig'], sim_film.name_orig)
            self.assertEqual(film['release_date'], sim_film.release_date)
            self.assertEqual(film['ratings']['kp'][0], sim_film.rating_kinopoisk)
            self.assertEqual(film['ratings']['kp'][1], sim_film.rating_kinopoisk_cnt)
            self.assertEqual(film['ratings']['imdb'][0], sim_film.rating_imdb)
            self.assertEqual(film['ratings']['imdb'][1], sim_film.rating_imdb_cnt)
            self.assertEqual(film['ratings']['cons'][0], 0)
            self.assertEqual(film['ratings']['cons'][1], 0)
            self.assertEqual(film['duration'], sim_film.duration)
            self.assertEqual(film['relation'], [])

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
        if len(response.data) != len(locations):
                self.assertTrue(False)
        for i in range(len(response.data)):
                self.assertEqual(response.data[i]['id'], locations[i].id)
                self.assertEqual(response.data[i]['type'], locations[i].type)
                self.assertEqual(response.data[i]['lang'], locations[i].lang)
                self.assertEqual(response.data[i]['quality'], locations[i].quality)
                self.assertEqual(response.data[i]['subtitles'], locations[i].subtitles)
                self.assertEqual(response.data[i]['price'], locations[i].price)
                self.assertEqual(response.data[i]['price_type'], locations[i].price_type)
                self.assertEqual(response.data[i]['url_view'], locations[i].url_view)

    def test_api_extras_ok(self):
        film = self.films[0]
        response = self.client.post(reverse('film_extras_view', kwargs={'film_id': film.id, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_extras_404(self):
        response = self.client.post(reverse('film_extras_view', kwargs={'film_id': 0, 'format': 'json'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_extras_without_type_data(self):
        film = self.films[0]
        extras = []
        for ext in self.extras:
            if film.id == ext.film.id:
                extras.append(ext)
        response = self.client.post(reverse('film_extras_view', kwargs={'film_id': film.id, 'format': 'json'}))
        if len(response.data) != len(extras):
            self.assertTrue(False)
        for i in range(len(response.data)):
            self.assertEqual(response.data[i]['id'], extras[i].id)
            self.assertEqual(response.data[i]['name'], extras[i].name)
            self.assertEqual(response.data[i]['name_orig'], extras[i].name_orig)
            self.assertEqual(response.data[i]['type'], extras[i].type)
            self.assertEqual(response.data[i]['url'], extras[i].url)
            self.assertEqual(response.data[i]['description'], extras[i].description)

    def test_api_extras_type_poster_data(self):
        film = self.films[0]
        extras = []
        data = {'type': APP_FILM_TYPE_ADDITIONAL_MATERIAL_POSTER}
        for ext in self.extras:
            if film.id == ext.film.id:
                extras.append(ext)
        response = self.client.post(reverse('film_extras_view', kwargs={'film_id': film.id, 'format': 'json'}), data=data)
        if len(response.data) != len(extras):
            self.assertTrue(False)
        for i in range(len(response.data)):
            self.assertEqual(response.data[i]['id'], extras[i].id)
            self.assertEqual(response.data[i]['name'], extras[i].name)
            self.assertEqual(response.data[i]['name_orig'], extras[i].name_orig)
            self.assertEqual(response.data[i]['type'], extras[i].type)
            self.assertEqual(response.data[i]['url'], extras[i].url)
            self.assertEqual(response.data[i]['description'], extras[i].description)

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
