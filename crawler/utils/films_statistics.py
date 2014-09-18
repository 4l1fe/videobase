# coding: utf-8
from apps.films.models import Films, Countries
from django.utils.datetime_safe import datetime, date
from django.utils import timezone


def film_statistics():
    count_films = Films.objects.count()
    no_description_count = 0
    kinopoisk_id_count = 0
    imdb_id_count = 0
    release_date_count = 0
    count_films_no_name = 0
    for i in range(1, count_films):
        try:
            film = Films.objects.get(id=i)
            countries = Countries.objects.get(id=film.countries._fk_val)
            if countries.name == u'Флатландию':
                count_films_no_name += 1
            if film.description == '':
                no_description_count += 1
            if not(film.kinopoisk_id is None):
                kinopoisk_id_count += 1
            if not(film.imdb_id is None):
                imdb_id_count += 1
            if not(film.release_date == date(2014, 01, 1)):
                release_date_count += 1
        except Films.DoesNotExist, e:
            import traceback
            traceback.print_exc()
    print u'Колличетсво фильмов без указанной страны:' + str(count_films_no_name)
    print u'Колличетсво фильмов без описания:' + str(no_description_count)
    print u'Колличетсво фильмов с кинопоиск id:' + str(kinopoisk_id_count)
    print u'Колличетсво фильмов с imdb id:' + str(imdb_id_count)
    print u'Колличетсво фильмов с датой выпуска:' + str(release_date_count)


def film_at_least_years_old(film, years):
    '''
    Returns true if @film less than @years old
    '''
    if film.release_date:
        return timezone.now().date() - film.release_date < timezone.timedelta(days=365*years)
    else:
        return True


