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
            ('frelease_date', self.gf('django.db.models.fields.DateField')()),
            ('fduration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('fbudget', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('rating_local', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('rating_local_cnt', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('rating_imdb', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('rating_imdb_cnt', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('kinopoisk_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('age_limit', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('kinopoisk_lastupdate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('rating_kinopoisk', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('rating_kinopoisk_cnt', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('seasons_cnt', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
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

        # Adding model 'FilmExtras'
        db.create_table('films_extras', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['films.Films'])),
            ('etype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
        ))
        db.send_create_signal(u'films', ['FilmExtras'])

        # Adding model 'UsersFilms'
        db.create_table('users_films', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'])),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['films.Films'])),
            ('ufstatus', self.gf('django.db.models.fields.IntegerField')()),
            ('ufrating', self.gf('django.db.models.fields.IntegerField')()),
            ('subscribed', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'films', ['UsersFilms'])

        # Adding model 'Seasons'
        db.create_table('seasons', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['films.Films'])),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('series_cnt', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'films', ['Seasons'])

        # Adding unique constraint on 'Seasons', fields ['film', 'number']
        db.create_unique('seasons', ['film_id', 'number'])


    def backwards(self, orm):
        # Removing unique constraint on 'Seasons', fields ['film', 'number']
        db.delete_unique('seasons', ['film_id', 'number'])

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

        # Deleting model 'FilmExtras'
        db.delete_table('films_extras')

        # Deleting model 'UsersFilms'
        db.delete_table('users_films')

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
            'etype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        u'films.films': {
            'Meta': {'object_name': 'Films', 'db_table': "'films'"},
            'age_limit': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'countries'", 'symmetrical': 'False', 'to': u"orm['films.Countries']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'fbudget': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fduration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'frelease_date': ('django.db.models.fields.DateField', [], {}),
            'ftype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'genres'", 'symmetrical': 'False', 'to': u"orm['films.Genres']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kinopoisk_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'kinopoisk_lastupdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'rating_imdb': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rating_imdb_cnt': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating_kinopoisk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rating_kinopoisk_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating_local': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rating_local_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seasons_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'films.genres': {
            'Meta': {'object_name': 'Genres', 'db_table': "'genres'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'films.seasons': {
            'Meta': {'unique_together': "(('film', 'number'),)", 'object_name': 'Seasons', 'db_table': "'seasons'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'series_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'films.usersfilms': {
            'Meta': {'object_name': 'UsersFilms', 'db_table': "'users_films'"},
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscribed': ('django.db.models.fields.IntegerField', [], {}),
            'ufrating': ('django.db.models.fields.IntegerField', [], {}),
            'ufstatus': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Users']"})
        },
        u'users.users': {
            'Meta': {'object_name': 'Users', 'db_table': "'users'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_visited': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'userpic': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['users.UsersPics']", 'null': 'True', 'blank': 'True'}),
            'userpic_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ustatus': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        u'users.userspics': {
            'Meta': {'object_name': 'UsersPics', 'db_table': "'users_pics'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Users']"})
        }
    }

    complete_apps = ['films']