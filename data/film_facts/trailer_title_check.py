# coding: utf-8


def is_correct_trailer_title(title, film):
    film_name = film.name.lower().encode("utf-8")
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
        check_has_many_useless_words = False
        ru_match = u''
        en_match = u''
        for index, phrase in trailers_ru_mask:
            if title.find(phrase) != -1:
                check_ru = True
                ru_match = trailers_ru_mask[index]

        for index, phrase in trailers_en_mask:
            if title.find(phrase) != -1:
                check_en = True
                en_match = trailers_en_mask[index]

        for phrase in trailers_block:
            if title.find(phrase) != -1:
                check_block = True

        tr_t_for_comparison = title.lower().encode("utf-8")
        if tr_t_for_comparison.find(film_name) != -1:
            check_fname = True

        if tr_t_for_comparison.find(str(film_year)) != -1:
            check_fyear = True

        if trailers_ru_mask or trailers_en_mask and not check_block: #проверяем много ли лишних слов помимо шаблонных
            cutted_title = title.Replace(en_match, '').Replace(ru_match, '').Replace(film_name, '').Replace(str(film_year), '').split(' ')
            if len(cutted_title)>3:
                check_has_many_useless_words = True
            else:
                check_has_many_useless_words = False
        print "ru:",check_ru, "en:",en_match, "name:",check_fname, "year:",check_fyear, "block:", check_block, "useless_words:", check_has_many_useless_words
        if (check_ru or check_en) and check_fname and check_fyear and not check_block and not check_has_many_useless_words:
            return True
        else:
            return False
    except Exception, ex:
        return True

