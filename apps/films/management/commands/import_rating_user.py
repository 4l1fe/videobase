# coding: utf-8

import os
import sys
import csv
import json
import codecs
from optparse import make_option

from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.management.base import BaseCommand

from rest_framework.authtoken.models import Token

from apps.films.models import Films
from apps.users.models import SessionToken, UsersApiSessions, User


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-f', '--filename',
                    action='store',
                    dest='filename',
                    default=False,
                    help='Full path for file',
                    ),
        make_option('-u', '--user',
                    action='store',
                    dest='user',
                    default=False,
                    help='ID for user',
                    ),
    )

    help = u"Импортирование оценок фильма из файла"
    requires_model_validation = True


    def handle(self, *args, **options):
        filename = options.get('filename', False)
        user_id = options.get('user', False)

        # Проверка имени файла
        if not filename:
            self.stdout.write(u'Введите имя файла')
            sys.exit(1)

        # Проверка пользователя
        if not user_id:
            self.stdout.write(u'Введите ID пользователя')
            sys.exit(1)

        # Проверка существования файла
        if os.path.exists(filename):
            self.stdout.write(u'Start: Import ratings from {0}'.format(filename))
            self.import_file(filename, user_id)
        else:
            raise Exception(u'File {0} not found'.format(filename))


    def import_file(self, filename, user_id):
        self.stdout.write(u'Run import - {0}'.format(filename))

        # Init data
        counter = 0
        not_linked_films = []
        o_user = User.objects.get(id=user_id)

        # Create Session
        token = Token.objects.get(user=o_user.id)
        s_token = SessionToken.objects.create(user=o_user)
        UsersApiSessions.objects.create(token=s_token)

        # Init Request
        request = Client(HTTP_X_MI_SESSION=s_token.key, HTTP_USER_AGENT='Mozilla/5.0')

        # Разбор файла
        data = self.__csvfile(filename)

        for row in data:
            list_film_id = Films.objects.filter(kinopoisk_id=row[0]).values_list('id', flat=True)
            if len(list_film_id) == 1:
                film_id = list_film_id[0]

                # Формирование запроса
                output = request.put(
                    reverse('act_film_rate_view', kwargs={'film_id': film_id, 'format': 'json'}),
                    json.dumps({'rating': row[1]}), content_type='application/json'
                )

                # Анализ ответа
                if output.status_code != 200:
                    self.stdout.write(u'Error: Film ID:{0}'.format(film_id))

            elif len(list_film_id) == 0:
                not_linked_films.append(row[0])
                self.stdout.write(u'Into Kinopoisk ID:{0} not linked with our films'.format(row[0]))

            else:
                raise Exception(u'Into one Kinopoisk ID:{0} linked with several films'.format(list_film_id))

            counter += 1
            if (counter % 100) == 0:
                self.stdout.write(u'Inserted {0} items'.format(counter))

        self.stdout.write(u'Inserted {0} items'.format(counter))
        self.stdout.write(u'Not linked films: {0}'.format(not_linked_films))


    def __csvfile(self, datafile):
        csvfile = codecs.open(datafile, 'r')
        return list(self.charset_csv_reader(csv_data=csvfile, charset='utf-8'))


    def charset_csv_reader(self, csv_data, dialect=csv.excel, charset='utf-8', **kwargs):
        csv_reader = csv.reader(csv_data, dialect=dialect, delimiter=',', lineterminator="\r\n", **kwargs)

        for row in csv_reader:
            yield [cell for cell in row]
