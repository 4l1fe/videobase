# coding: utf-8
from rest_framework import serializers
from django.db.models import Q
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
        genre_films_count = Films.objects.filter(Q(uf_films_rel__user=self.user), Q(genres=obj), ~Q(uf_films_rel__status=APP_USERFILM_STATUS_NOT_WATCH)).count()
        return round((float(genre_films_count) / float(self.user_films_count)) * 100, 1) if self.user_films_count else 0

    class Meta:
        model = Genres
        fields = ('id', 'name', 'percent')
