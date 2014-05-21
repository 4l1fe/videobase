# coding: utf-8
from rest_framework import serializers

from apps.films.models import Genres, UsersFilms, Films
from apps.films.constants import APP_USERFILM_STATUS_NOT_WATCH


class vbUserGenre(serializers.ModelSerializer):
    percent = serializers.SerializerMethodField('calc_percent')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        if self.user is None:
            raise ValueError("Haven't user object")
        super(vbUserGenre, self).__init__(*args, **kwargs)
        self.user_films_count = self._get_films_count()

    def _get_films_count(self):
        return UsersFilms.objects.filter(user=self.user).exclude(status=APP_USERFILM_STATUS_NOT_WATCH).count()

    def calc_percent(self, obj):
        genre_films_count = Films.objects.filter(users_films__user=self.user, genres=obj).exclude(users_films__status=APP_USERFILM_STATUS_NOT_WATCH).count()
        return (float(genre_films_count) / float(self.user_films_count)) * 100

    class Meta:
        model = Genres
        fields = ('id', 'name', 'percent')
