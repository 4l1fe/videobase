# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FilmExtras.photo'
        db.add_column('films_extras', 'photo',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FilmExtras.photo'
        db.delete_column('films_extras', 'photo')


    models = {
        'films.countries': {
            'Meta': {'object_name': 'Countries', 'db_table': "'countries'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'films.filmextras': {
            'Meta': {'object_name': 'FilmExtras', 'db_table': "'films_extras'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'etype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'films.films': {
            'Meta': {'object_name': 'Films', 'db_table': "'films'"},
            'age_limit': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'countries'", 'symmetrical': 'False', 'to': "orm['films.Countries']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'fbudget': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fduration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'frelease_date': ('django.db.models.fields.DateField', [], {}),
            'ftype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'genres'", 'symmetrical': 'False', 'to': "orm['films.Genres']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
        'films.genres': {
            'Meta': {'object_name': 'Genres', 'db_table': "'genres'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'films.persons': {
            'Meta': {'object_name': 'Persons', 'db_table': "'persons'"},
            'bio': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'films.personsextras': {
            'Meta': {'object_name': 'PersonsExtras', 'db_table': "'persons_extras'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'etype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'name_orig': ('django.db.models.fields.TextField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Persons']", 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'films.personsfilms': {
            'Meta': {'unique_together': "(('film', 'person', 'p_type'),)", 'object_name': 'PersonsFilms', 'db_table': "'persons_films'"},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'p_character': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'p_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Persons']"})
        },
        'films.seasons': {
            'Meta': {'unique_together': "(('film', 'number'),)", 'object_name': 'Seasons', 'db_table': "'seasons'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'series_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'films.usersfilms': {
            'Meta': {'object_name': 'UsersFilms', 'db_table': "'users_films'"},
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscribed': ('django.db.models.fields.IntegerField', [], {}),
            'ufrating': ('django.db.models.fields.IntegerField', [], {}),
            'ufstatus': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Users']"})
        },
        'films.userspersons': {
            'Meta': {'object_name': 'UsersPersons', 'db_table': "'users_persons'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Persons']", 'max_length': '255'}),
            'subscribed': ('django.db.models.fields.IntegerField', [], {}),
            'upstatus': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Users']", 'max_length': '255'})
        },
        'users.users': {
            'Meta': {'object_name': 'Users', 'db_table': "'users'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_visited': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'userpic': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': "orm['users.UsersPics']"}),
            'userpic_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ustatus': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'users.userspics': {
            'Meta': {'object_name': 'UsersPics', 'db_table': "'users_pics'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Users']"})
        }
    }

    complete_apps = ['films']