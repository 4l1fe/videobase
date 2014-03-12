# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Films.poster_id'
        db.delete_column('films', 'poster_id')


        # Changing field 'Films.fReleaseDate'
        db.alter_column('films', 'fReleaseDate', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Films.poster_id'
        raise RuntimeError("Cannot reverse this migration. 'Films.poster_id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Films.poster_id'
        db.add_column('films', 'poster_id',
                      self.gf('django.db.models.fields.IntegerField')(),
                      keep_default=False)


        # Changing field 'Films.fReleaseDate'
        db.alter_column('films', 'fReleaseDate', self.gf('django.db.models.fields.DateTimeField')())

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
            'fReleaseDate': ('django.db.models.fields.DateField', [], {}),
            'ftype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'genres'", 'symmetrical': 'False', 'to': u"orm['films.Countries']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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