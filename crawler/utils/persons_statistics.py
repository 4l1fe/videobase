# coding: utf-8
from apps.films.models import Persons


def persons_statistics():
    count_persons = Persons.objects.count()
    count_bio = 0
    count_photo = 0
    count_birthdate = 0
    for i in range(1, count_persons):
        try:
            person = Persons.objects.get(id=i)
            if person.bio != '':
                count_bio += 1
            if person.photo != '':
                count_photo += 1
            if not(person.birthdate is None):
                count_birthdate += 1
        except Persons.DoesNotExist, e:
            print e
    print u'Колличество персон с биографией:' + str(count_bio)
    print u'Колличетсво персон с фотографией:' + str(count_photo)
    print u'Колличетсво персон с датой рождения:' + str(count_birthdate)

