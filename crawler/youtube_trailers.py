# coding: utf-8
'''

Необходимо создать робот поиска трейлеров на youtube.

Поиск по следующему алгоритму:

1. Поиск по Название фильма + "трейлер"
2. Если в п. 1 ничего не найдено, то Оригинальное название фильма + "трейлер"
3. Если в п. 2 ничего не найдено, то Оригинальное название фильма + "trailer"

Если трейлер не найден, то повторять поиск для фильмов:

1. Для фильмов с датой выхода больше текущей и фильмов не старше одного года - раз в день
2. Для фильмов не старше 3 лет - один раз в неделю
3. Для остальных фильмов - раз в месяц.

'''


import gdata.youtube
import gdata.youtube.service
from itertools import chain
from apps.films.models import YoutubeTrailerCheck
from apps.films.models import FilmExtras
from apps.films.constants import APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER
from django.utils import timezone

delays = (
    #1. Для фильмов с датой выхода больше текущей и фильмов не старше одного года - раз в день
    (timezone.timedelta(days=365), timezone.timedelta(days =1)),
    #2. Для фильмов не старше 3 лет - один раз в неделю
    (timezone.timedelta(days=365*3), timezone.timedelta(days =7)),
    #3. Для остальных фильмов - раз в месяц.
    (timezone.timedelta(days=365*3 +1), timezone.timedelta(days =1)),
)

SEARCH_STRINGS_RU = ('официальный русский трейлер фильма hd','русский трейлер фильма hd','русский трейлер HD','трейлер на русском','официальный трейлер','русский трейлер','тв-ролик','финальный трейлер','промо ролик')
SEARCH_STRINGS_EN =  ('international trailer hd', 'official trailer hd','trailer hd', 'international trailer', 'official teaser', 'trailer')
FAIL_STRINGS = ('interview','интервью','premiere','премьера','review','обзор','conference','behind the scenes','gameplay','parody','videogame')


def query_search(film_name,trailer_word):
    client = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()

    query.vq = (film_name + trailer_word).encode('utf-8')
    query.max_results = 25
    

    feed = client.YouTubeQuery(query)

    for f in feed.entry:
        
        title = f.title.text.lower().decode('utf-8')
        if (film_name.lower() in title) and (trailer_word.lower() in title and sum(s in title for s in FAIL_STRINGS)==0):
            yield f.title.text, f.link[0].href



def get_film_trailer(film):

    trailer_name,link = next(
        chain(
            chain(
                *(query_search(film.name,w) for w in SEARCH_STRINGS_RU)),
            
        chain(
            *(query_search(film.name_orig,w) for w in SEARCH_STRINGS_EN))
        ),
        None)
    
    return trailer_name,link
        
def process_film(film):

    try:
        ytchk= YoutubeTrailerCheck.objects.get(film = film)

    except YoutubeTrailerCheck.DoesNotExist:

        ytchk = YoutubeTrailerCheck(film=film,
                                    last_check=timezone.now() - timezone.timedelta(days = 1000),
                                    was_successfull =False

        )
        ytchk.save()


    if ytchk.was_successfull:
        print "Trailer already set"
        return
    else:
        for delta,delay in delays:
            
            if  timezone.now().date() - film.release_date < delta:

                if ytchk.last_check - timezone.now() < delay:

                    print "Trying to get trailer for {} from youtube".format(film)
                    trtuple = get_film_trailer(film)
                    if trtuple:
                        trailer_name, link = trtuple

                        fe = FilmExtras(film= film,
                                    type = APP_FILM_TYPE_ADDITIONAL_MATERIAL_TRAILER,
                                    name = trailer_name,
                                    name_orig = trailer_name,
                                    description = trailer_name,
                                    url = link )

                        fe.save()
                        ytchk.was_successfull = True
                        print "Succesfully set trailer"
                    else:
                        print "Failed to find trailer"
                        ytchk.was_successfull = False
                        
                    ytchk.last_check = timezone.now()
                    ytchk.save()
                return
                


        


    








    



    
    
    