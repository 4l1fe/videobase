#coding: utf-8
from apps.users.models.api_session import SessionToken, UsersApiSessions

__author__ = 'ipatov'
from apps.films.tests.factories import *
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse


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
        for i in range(2):
            self.persons.append(PersonFactory.create())
            self.films.append(FilmFactory.create(genres=(self.genres[2*i], self.genres[2*i+1]), countries=(self.countries[2*i], self.countries[2*i+1])))
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

    def test_api_action_comments(self):
        film = self.films[0]
        token = Token.objects.get(user=self.user)
        s_token = SessionToken.objects.create(user=self.user)
        UsersApiSessions.objects.create(token=s_token)
        headers = "%s %s" % ('X-VB-Token', s_token.key)
        response = self.client.post(reverse('act_film_comment_view', kwargs={'film_id': film.id, 'format': 'json'}), HTTP_AUTHORIZATION=headers, data={'text': u'Отличный фильм'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)