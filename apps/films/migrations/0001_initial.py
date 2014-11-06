# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.common
import djorm_pgfulltext.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0433\u043e\u0440\u043e\u0434\u0430', db_index=True)),
                ('name_orig', models.CharField(max_length=255, verbose_name='\u041e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0435 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0433\u043e\u0440\u043e\u0434\u0430')),
            ],
            options={
                'db_table': 'cities',
                'verbose_name': '\u0413\u043e\u0440\u043e\u0434',
                'verbose_name_plural': '\u0413\u043e\u0440\u043e\u0434\u0430',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u0420\u0443\u0441\u0441\u043a\u043e\u0435 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0440\u0430\u043d\u044b', db_index=True)),
                ('name_orig', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0440\u0430\u043d\u044b \u043d\u0430 \u0435\u0435 \u044f\u0437\u044b\u043a\u0435')),
                ('description', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
            ],
            options={
                'db_table': 'countries',
                'verbose_name': '\u0421\u0442\u0440\u0430\u043d\u0430',
                'verbose_name_plural': '\u0421\u0442\u0440\u0430\u043d\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FilmExtras',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(db_index=True, max_length=255, verbose_name='\u0422\u0438\u043f \u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0433\u043e \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u0430', choices=[(b'POSTER', '\u041f\u043e\u0441\u0442\u0435\u0440'), (b'TRAILER', '\u0422\u0440\u0435\u0439\u043b\u0435\u0440')])),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('name_orig', models.CharField(max_length=255, verbose_name='\u041e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0435 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('description', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('url', models.URLField(max_length=255, null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0434\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b', blank=True)),
                ('photo', models.ImageField(upload_to=utils.common.get_image_path, null=True, verbose_name='\u041f\u043e\u0441\u0442\u0435\u0440', blank=True)),
            ],
            options={
                'db_table': 'films_extras',
                'verbose_name': '\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b \u043a \u0444\u0438\u043b\u044c\u043c\u0443',
                'verbose_name_plural': '\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u044b \u043a \u0444\u0438\u043b\u044c\u043c\u0430\u043c',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Films',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0444\u0438\u043b\u044c\u043c\u0430', db_index=True)),
                ('type', models.CharField(db_index=True, max_length=255, verbose_name='\u0422\u0438\u043f \u0444\u0438\u043b\u044c\u043c\u0430', choices=[('FULL_FILM', '\u041f\u043e\u043b\u043d\u043e\u043c\u0435\u0442\u0440\u0430\u0436\u043d\u044b\u0439 \u0444\u0438\u043b\u044c\u043c'), ('SERIAL', '\u0421\u0435\u0440\u0438\u0430\u043b')])),
                ('world_release_date', models.DateField(db_index=True, null=True, verbose_name='\u041c\u0438\u0440\u043e\u0432\u0430\u044f \u0434\u0430\u0442\u0430 \u0432\u044b\u0445\u043e\u0434\u0430', blank=True)),
                ('release_date', models.DateField(db_index=True, null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0432\u044b\u0445\u043e\u0434\u0430', blank=True)),
                ('duration', models.IntegerField(null=True, verbose_name='\u041f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0444\u0438\u043b\u044c\u043c\u0430', blank=True)),
                ('budget', models.IntegerField(null=True, verbose_name='\u0411\u044e\u0434\u0436\u0435\u0442 \u0444\u0438\u043b\u044c\u043c\u0430', blank=True)),
                ('description', models.TextField(default=b'', verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0444\u0438\u043b\u044c\u043c\u0430', blank=True)),
                ('rating_local', models.FloatField(default=0, null=True, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433 \u0444\u0438\u043b\u044c\u043c\u0430 \u043f\u043e \u043c\u043d\u0435\u043d\u0438\u044e \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439 \u043d\u0430\u0448\u0435\u0433\u043e \u0441\u0430\u0439\u0442\u0430', db_index=True, blank=True)),
                ('rating_local_cnt', models.IntegerField(default=0, null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439 \u043d\u0430\u0448\u0435\u0433\u043e \u0441\u0430\u0439\u0442\u0430 \u043e\u0446\u0435\u043d\u0438\u0432\u0448\u0438\u0445 \u0444\u0438\u043b\u044c\u043c', db_index=True, blank=True)),
                ('imdb_id', models.IntegerField(null=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043a\u043e\u0432\u044b\u0439 \u043d\u043e\u043c\u0435\u0440 \u043d\u0430 IMDB', blank=True)),
                ('rating_imdb', models.FloatField(default=0, null=True, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433 \u0444\u0438\u043b\u044c\u043c\u0430 \u043d\u0430 \u0441\u0430\u0439\u0442\u0435 imdb.com', blank=True)),
                ('rating_imdb_cnt', models.PositiveIntegerField(default=0, null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439 imdb.com \u043e\u0446\u0435\u043d\u0438\u0432\u0448\u0438\u0445 \u044d\u0442\u043e\u0442 \u0444\u0438\u043b\u044c\u043c', blank=True)),
                ('rating_cons', models.FloatField(default=0, null=True, verbose_name='\u041a\u043e\u043d\u0441\u043e\u043b\u0438\u0434\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u0440\u0435\u0439\u0442\u0438\u043d\u0433', blank=True)),
                ('rating_cons_cnt', models.PositiveIntegerField(default=0, null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0433\u043e\u043b\u043e\u0441\u043e\u0432 \u043a\u043e\u043d\u0441\u043e\u043b\u0438\u0434\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u043e\u0433\u043e \u0440\u0435\u0439\u0442\u0438\u043d\u0433\u0430', db_index=True, blank=True)),
                ('rating_sort', models.IntegerField(default=0, null=True, verbose_name='\u0423\u0441\u043b\u043e\u0432\u043d\u044b\u0439 \u0440\u0435\u0439\u0442\u0438\u043d\u0433 \u0434\u043b\u044f \u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u043a\u0438', db_index=True, blank=True)),
                ('kinopoisk_id', models.IntegerField(unique=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043a\u043e\u0432\u044b\u0439 \u043d\u043e\u043c\u0435\u0440 \u043d\u0430 \u043a\u0438\u043d\u043e\u043f\u043e\u0438\u0441\u043a\u0435', db_index=True)),
                ('age_limit', models.PositiveSmallIntegerField(db_index=True, null=True, verbose_name='\u041e\u0433\u0440\u0430\u043d\u0438\u0447\u0435\u043d\u0438\u0435 \u043f\u043e \u0432\u043e\u0437\u0440\u0430\u0441\u0442\u0443', blank=True)),
                ('kinopoisk_lastupdate', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0433\u043e \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f \u043d\u0430 \u043a\u0438\u043d\u043e\u043f\u043e\u0438\u0441\u043a\u0435', blank=True)),
                ('rating_kinopoisk', models.FloatField(null=True, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433 \u0444\u0438\u043b\u044c\u043c\u0430 \u043d\u0430 \u0441\u0430\u0439\u0442\u0435 kinopoisk.ru', blank=True)),
                ('rating_kinopoisk_cnt', models.PositiveIntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439 kinopoisk.ru \u043e\u0446\u0435\u043d\u0438\u0432\u0448\u0438\u0445 \u044d\u0442\u043e\u0442 \u0444\u0438\u043b\u044c\u043c', blank=True)),
                ('seasons_cnt', models.PositiveSmallIntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0441\u0435\u0437\u043e\u043d\u043e\u0432', blank=True)),
                ('name_orig', models.CharField(default=b'', max_length=255, verbose_name='\u041e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0435 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0444\u0438\u043b\u044c\u043c\u0430', db_index=True, blank=True)),
                ('was_shown', models.BooleanField(default=False, verbose_name='\u0424\u0438\u043b\u044c\u043c \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u043b\u0441\u044f \u0432 \u043d\u043e\u0432\u0438\u043d\u043a\u0430\u0445')),
                ('subscribed_cnt', models.PositiveIntegerField(default=0, null=True, verbose_name='\u041a\u043e\u043b-\u0432\u043e \u043f\u043e\u0434\u043f\u0438\u0441\u0447\u0438\u043a\u043e\u0432', db_index=True, blank=True)),
                ('search_index', djorm_pgfulltext.fields.VectorField(default=b'', serialize=False, null=True, editable=False, db_index=True)),
                ('countries', models.ManyToManyField(related_name='countries', verbose_name='\u0421\u0442\u0440\u0430\u043d\u044b \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u0438', to='films.Countries')),
            ],
            options={
                'db_table': 'films',
                'verbose_name': '\u0424\u0438\u043b\u044c\u043c',
                'verbose_name_plural': '\u0424\u0438\u043b\u044c\u043c\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lft', models.PositiveIntegerField(db_index=True)),
                ('rgt', models.PositiveIntegerField(db_index=True)),
                ('tree_id', models.PositiveIntegerField(db_index=True)),
                ('depth', models.PositiveIntegerField(db_index=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0436\u0430\u043d\u0440\u0430', db_index=True)),
                ('description', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0436\u0430\u043d\u0440\u0430')),
                ('hidden', models.NullBooleanField(default=False, verbose_name='\u0421\u043a\u0440\u044b\u0442\u044b\u0439', db_index=True)),
            ],
            options={
                'db_table': 'genres',
                'verbose_name': '\u0416\u0430\u043d\u0440',
                'verbose_name_plural': '\u0416\u0430\u043d\u0440\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u0418\u043c\u044f', db_index=True)),
                ('name_orig', models.CharField(max_length=255, verbose_name='\u041e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0435 \u0438\u043c\u044f', db_index=True)),
                ('bio', models.TextField(verbose_name='\u0411\u0438\u043e\u0433\u0440\u0430\u0444\u0438\u044f')),
                ('photo', models.ImageField(upload_to=utils.common.get_image_path, null=True, verbose_name='\u0424\u043e\u0442\u043e', blank=True)),
                ('birthdate', models.DateField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043d\u044f \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f', blank=True)),
                ('kinopoisk_id', models.IntegerField(unique=True)),
                ('city', models.ForeignKey(related_name='persons', verbose_name='\u0413\u043e\u0440\u043e\u0434', blank=True, to='films.Cities', null=True)),
            ],
            options={
                'db_table': 'persons',
                'verbose_name': '\u041f\u0435\u0440\u0441\u043e\u043d\u0430',
                'verbose_name_plural': '\u041f\u0435\u0440\u0441\u043e\u043d\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonsExtras',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=255, verbose_name='', db_index=True)),
                ('name', models.TextField(verbose_name='\u0418\u043c\u044f')),
                ('name_orig', models.TextField(verbose_name='\u041e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0435 \u0438\u043c\u044f')),
                ('description', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('url', models.CharField(max_length=255, verbose_name='\u0424\u043e\u0442\u043e')),
                ('person', models.ForeignKey(verbose_name='\u041f\u0435\u0440\u0441\u043e\u043d\u0430', to='films.Persons', max_length=255)),
            ],
            options={
                'db_table': 'persons_extras',
                'verbose_name': '\u0420\u0430\u0441\u0448\u0438\u0440\u0435\u043d\u0438\u044f \u043f\u0435\u0440\u0441\u043e\u043d\u044b',
                'verbose_name_plural': '\u0420\u0430\u0441\u0448\u0438\u0440\u0435\u043d\u0438\u044f \u043f\u0435\u0440\u0441\u043e\u043d',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonsFilms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('p_type', models.CharField(db_index=True, max_length=255, verbose_name='\u0422\u0438\u043f \u043f\u0435\u0440\u0441\u043e\u043d\u044b', choices=[(b'actor', '\u0410\u043a\u0442\u0435\u0440'), (b'producer', '\u041f\u0440\u043e\u0434\u044e\u0441\u0435\u0440'), (b'director', '\u0420\u0435\u0436\u0438\u0441\u0441\u0435\u0440'), (b'scriptwriter', '\u0421\u0446\u0435\u043d\u0430\u0440\u0438\u0441\u0442')])),
                ('p_index', models.IntegerField(default=0, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a \u043d\u0430 \u043a\u0438\u043d\u043e\u043f\u043e\u0438\u0441\u043a\u0435', db_index=True)),
                ('p_character', models.CharField(default=b'', max_length=255)),
                ('description', models.CharField(default=b'', max_length=255)),
                ('film', models.ForeignKey(related_name='pf_films_rel', verbose_name='\u0424\u0438\u043b\u044c\u043c', to='films.Films')),
                ('person', models.ForeignKey(related_name='pf_persons_rel', verbose_name='\u041f\u0435\u0440\u0441\u043e\u043d\u0430', to='films.Persons')),
            ],
            options={
                'db_table': 'persons_films',
                'verbose_name': '\u0420\u043e\u043b\u044c \u043f\u0435\u0440\u0441\u043e\u043d\u044b \u0432 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0435 \u0444\u0438\u043b\u044c\u043c\u0430',
                'verbose_name_plural': '\u0420\u043e\u043b\u0438 \u043f\u0435\u0440\u0441\u043e\u043d \u0432 \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0435 \u0444\u0438\u043b\u044c\u043c\u043e\u0432',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Seasons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('release_date', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0432\u044b\u0445\u043e\u0434\u0430 \u0441\u0435\u0437\u043e\u043d\u0430')),
                ('series_cnt', models.PositiveSmallIntegerField(verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0441\u0435\u0440\u0438\u0439 \u0432 \u0441\u0435\u0437\u043e\u043d\u0435')),
                ('description', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0441\u0435\u0437\u043e\u043d\u0430')),
                ('number', models.PositiveSmallIntegerField(verbose_name='\u041f\u043e\u0440\u044f\u0434\u043a\u043e\u0432\u044b\u0439 \u043d\u043e\u043c\u0435\u0440 \u0441\u0435\u0437\u043e\u043d\u0430')),
                ('film', models.ForeignKey(verbose_name='\u0424\u0438\u043b\u044c\u043c', to='films.Films')),
            ],
            options={
                'db_table': 'seasons',
                'verbose_name': '\u0421\u0435\u0437\u043e\u043d',
                'verbose_name_plural': '\u0421\u0435\u0437\u043e\u043d\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersFilms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(default=0, choices=[(0, '\u041d\u0435 \u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u043e'), (1, '\u041d\u0435 \u0431\u0443\u0434\u0443 \u0441\u043c\u043e\u0442\u0440\u0435\u0442\u044c'), (2, '\u0412 \u043f\u043b\u0435\u0439\u043b\u0438\u0441\u0442\u0435')], blank=True, null=True, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0444\u0438\u043b\u044c\u043c\u0430 \u0441 \u0442.\u0437. \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', db_index=True)),
                ('rating', models.PositiveSmallIntegerField(db_index=True, null=True, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433 \u0444\u0438\u043b\u044c\u043c\u0430 \u043f\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u044b\u0439 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u043c', blank=True)),
                ('subscribed', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u043f\u043e\u0434\u043f\u0438\u0441\u043a\u0438', blank=True, choices=[(0, '\u041d\u0435 \u043f\u043e\u0434\u043f\u0438\u0441\u0430\u043d'), (1, '\u041f\u043e\u0434\u043f\u0438\u0441\u0430\u043d')])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('film', models.ForeignKey(related_name='uf_films_rel', verbose_name='\u0424\u0438\u043b\u044c\u043c', to='films.Films')),
                ('user', models.ForeignKey(related_name='uf_users_rel', verbose_name='\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043b\u044f', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users_films',
                'verbose_name': '\u0424\u0438\u043b\u044c\u043c\u044b \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u0424\u0438\u043b\u044c\u043c\u044b \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersPersons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upstatus', models.IntegerField(default=0, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441')),
                ('subscribed', models.IntegerField(default=0, verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u043a\u0430', choices=[(0, '\u041d\u0435 \u043f\u043e\u0434\u043f\u0438\u0441\u0430\u043d'), (1, '\u041f\u043e\u0434\u043f\u0438\u0441\u0430\u043d')])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('person', models.ForeignKey(related_name='up_persons_rel', verbose_name='\u041f\u0435\u0440\u0441\u043e\u043d\u0430', to='films.Persons', max_length=255)),
                ('user', models.ForeignKey(related_name='up_users_rel', verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL, max_length=255)),
            ],
            options={
                'db_table': 'users_persons',
                'verbose_name': '\u041f\u0435\u0440\u0441\u043e\u043d\u044b \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u041f\u0435\u0440\u0441\u043e\u043d\u044b \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='YoutubeTrailerCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_check', models.DateTimeField(verbose_name='Last try datetime')),
                ('was_successfull', models.BooleanField(default=False, verbose_name='Was finding a trailer succesfull')),
                ('film', models.ForeignKey(verbose_name='Film', to='films.Films')),
            ],
            options={
                'db_table': 'youtube_trailer_check',
                'verbose_name': 'Youtube try',
                'verbose_name_plural': 'Youtube tries',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='usersfilms',
            unique_together=set([('user', 'film')]),
        ),
        migrations.AlterUniqueTogether(
            name='seasons',
            unique_together=set([('film', 'number')]),
        ),
        migrations.AlterUniqueTogether(
            name='personsfilms',
            unique_together=set([('film', 'person', 'p_type')]),
        ),
        migrations.AddField(
            model_name='films',
            name='genres',
            field=models.ManyToManyField(related_name='genres', verbose_name='\u0416\u0430\u043d\u0440\u044b', to='films.Genres'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='films',
            name='persons',
            field=models.ManyToManyField(related_name='persons', verbose_name='\u041f\u0435\u0440\u0441\u043e\u043d\u044b', through='films.PersonsFilms', to='films.Persons'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='filmextras',
            name='film',
            field=models.ForeignKey(related_name='fe_film_rel', verbose_name='\u0424\u0438\u043b\u044c\u043c', to='films.Films'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cities',
            name='country',
            field=models.ForeignKey(related_name='cities', verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0440\u0430\u043d\u044b', to='films.Countries'),
            preserve_default=True,
        ),
    ]
