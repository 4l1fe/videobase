# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Countries'
        db.create_table('countries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'films', ['Countries'])

        # Adding model 'Genres'
        db.create_table('genres', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'films', ['Genres'])

        # Adding model 'Films'
        db.create_table('films', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ftype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fReleaseDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('rating_local', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('rating_local_cnt', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('rating_imdb', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('rating_imdb_cnt', self.gf('django.db.models.fields.IntegerField')()),
            ('rating_kinopoisk', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('rating_kinopoisk_cnt', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('seasons_cnt', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('name_orig', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('poster_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'films', ['Films'])

        # Adding M2M table for field countries on 'Films'
        m2m_table_name = db.shorten_name('films_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('films', models.ForeignKey(orm[u'films.films'], null=False)),
            ('countries', models.ForeignKey(orm[u'films.countries'], null=False))
        ))
        db.create_unique(m2m_table_name, ['films_id', 'countries_id'])

        # Adding M2M table for field genres on 'Films'
        m2m_table_name = db.shorten_name('films_genres')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('films', models.ForeignKey(orm[u'films.films'], null=False)),
            ('genres', models.ForeignKey(orm[u'films.genres'], null=False))
        ))
        db.create_unique(m2m_table_name, ['films_id', 'genres_id'])

        # Adding model 'UsersFilms'
        db.create_table('users_films', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('users', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'])),
            ('films', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['films.Films'])),
            ('ufStatus', self.gf('django.db.models.fields.IntegerField')()),
            ('ufRating', self.gf('django.db.models.fields.IntegerField')()),
            ('subscribed', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'films', ['UsersFilms'])

        # Adding model 'FilmExtras'
        db.create_table('films_extras', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['films.Films'])),
            ('eType', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
        ))
        db.send_create_signal(u'films', ['FilmExtras'])

        # Adding model 'Seasons'
        db.create_table('seasons', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['films.Films'])),
            ('sReleaseDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('series_cnt', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('sNumber', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'films', ['Seasons'])


    def backwards(self, orm):
        # Deleting model 'Countries'
        db.delete_table('countries')

        # Deleting model 'Genres'
        db.delete_table('genres')

        # Deleting model 'Films'
        db.delete_table('films')

        # Removing M2M table for field countries on 'Films'
        db.delete_table(db.shorten_name('films_countries'))

        # Removing M2M table for field genres on 'Films'
        db.delete_table(db.shorten_name('films_genres'))

        # Deleting model 'UsersFilms'
        db.delete_table('users_films')

        # Deleting model 'FilmExtras'
        db.delete_table('films_extras')

        # Deleting model 'Seasons'
        db.delete_table('seasons')


    models = {
        u'films.countries': {
            'Meta': {'object_name': 'Countries', 'db_table': "'countries'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'films.filmextras': {
            'Meta': {'object_name': 'FilmExtras', 'db_table': "'films_extras'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'eType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        u'films.films': {
            'Meta': {'object_name': 'Films', 'db_table': "'films'"},
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'countries'", 'symmetrical': 'False', 'to': u"orm['films.Countries']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'fReleaseDate': ('django.db.models.fields.DateTimeField', [], {}),
            'ftype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'genres'", 'symmetrical': 'False', 'to': u"orm['films.Countries']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'poster_id': ('django.db.models.fields.IntegerField', [], {}),
            'rating_imdb': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'rating_imdb_cnt': ('django.db.models.fields.IntegerField', [], {}),
            'rating_kinopoisk': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'rating_kinopoisk_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'rating_local': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'rating_local_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'seasons_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'films.genres': {
            'Meta': {'object_name': 'Genres', 'db_table': "'genres'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'films.seasons': {
            'Meta': {'object_name': 'Seasons', 'db_table': "'seasons'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sNumber': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sReleaseDate': ('django.db.models.fields.DateTimeField', [], {}),
            'series_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'films.usersfilms': {
            'Meta': {'object_name': 'UsersFilms', 'db_table': "'users_films'"},
            'films': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscribed': ('django.db.models.fields.IntegerField', [], {}),
            'ufRating': ('django.db.models.fields.IntegerField', [], {}),
            'ufStatus': ('django.db.models.fields.IntegerField', [], {}),
            'users': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Users']"})
        },
        u'users.users': {
            'Meta': {'object_name': 'Users', 'db_table': "'users'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_visited': ('django.db.models.fields.DateTimeField', [], {}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'passhash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'userpic_id': ('django.db.models.fields.IntegerField', [], {}),
            'userpic_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ustatus': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['films']