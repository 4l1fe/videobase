# coding: utf-8
from data.unicode_convertor import convert_to_unicode


def is_correct_trailer_title(title, film):
    title = convert_to_unicode(title).lower()
    film_name = film.name.lower()
    film_year = film.release_date.year
    try:
        trailers_ru_mask = [u'официальный русский трейлер фильма hd',u'русский трейлер фильма hd', u'русский трейлер HD',
                            u'трейлер на русском', u'официальный трейлер',u'русский трейлер',u'тв-ролик', u'финальный трейлер', u'промо ролик' ]
        trailers_en_mask = [u'international trailer hd', u'official trailer hd', u'trailer hd', u'international trailer', u'official teaser', u'trailer']
        trailers_block = [u'interview', u'интервью', u'premiere', u'премьера',u'review', u'обзор', u'conference', u'behind the scenes', u'gameplay', u'parody', u'videogame' ]
        check_ru = False
        check_en = False
        check_block = False
        check_fname = False
        check_fyear = False
        for phrase in trailers_ru_mask:
            if title.find(phrase) != -1:
                check_ru = True

        for phrase in trailers_en_mask:
            if title.find(phrase) != -1:
                check_en = True

        for phrase in trailers_block:
            if title.find(phrase) != -1:
                check_block = True

        if title.find(film_name) != -1:
            check_fname = True

        if title.find(str(film_year)) != -1:
            check_fyear = True
        if (check_ru or check_en) and check_fname and check_fyear and not check_block:
            return True
        else:
            return False
    except ValueError, ex:
        print "Trailer checking failed ", ex.message
        return True

