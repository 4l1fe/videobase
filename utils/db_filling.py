#coding: utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videobase.settings")

from apps.films.models.persons_films import PersonsFilms
from apps.films.constants import APP_FILM_PERSON_TYPES
from datetime import datetime
from random import choice


def change_persons_roles():
    """Изначально в таблице persons_films в поле p_type были значения только - "actor".
    Для того, чтобы сэмулировать чуть более реальные данные,
    заполняем записи таблички произвольно всеми ролями из APP_FILM_PERSON_TYPES"""

    pf_count = PersonsFilms.objects.count()  # 280408

    choices = range(1, pf_count)
    chunk = pf_count/len(APP_FILM_PERSON_TYPES)

    for role in APP_FILM_PERSON_TYPES:
        filtered_pf = []
        for i in range(chunk):
            try:
                pf_pk = choice(choices)
                filtered_pf.append(pf_pk)
                choices.remove(pf_pk)
            except IndexError:
                break
        PersonsFilms.objects.filter(pk__in=filtered_pf).update(p_type=role[0])


if __name__ == '__main__':
    start = datetime.now()
    change_persons_roles()
    end = datetime.now()
    print(u'Изменение ролей длилось: {}'.format((end-start).total_seconds()))

