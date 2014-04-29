# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'RobotsTries.url'
        db.alter_column('robots_tries', 'url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True))

    def backwards(self, orm):

        # Changing field 'RobotsTries.url'
        db.alter_column('robots_tries', 'url', self.gf('django.db.models.fields.URLField')(default='', max_length=255))

    models = {
        'films.cities': {
            'Meta': {'object_name': 'Cities', 'db_table': "'cities'"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'to': "orm['films.Countries']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'films.countries': {
            'Meta': {'object_name': 'Countries', 'db_table': "'countries'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'films.films': {
            'Meta': {'object_name': 'Films', 'db_table': "'films'"},
            'age_limit': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'budget': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'countries'", 'symmetrical': 'False', 'to': "orm['films.Countries']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'genres'", 'symmetrical': 'False', 'to': "orm['films.Genres']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'kinopoisk_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'kinopoisk_lastupdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'persons': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'persons'", 'symmetrical': 'False', 'through': "orm['films.PersonsFilms']", 'to': "orm['films.Persons']"}),
            'rating_cons': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rating_cons_cnt': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rating_imdb': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rating_imdb_cnt': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating_kinopoisk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rating_kinopoisk_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating_local': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rating_local_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {}),
            'seasons_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'city': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'persons'", 'null': 'True', 'to': "orm['films.Cities']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'films.personsfilms': {
            'Meta': {'unique_together': "(('film', 'person', 'p_type'),)", 'object_name': 'PersonsFilms', 'db_table': "'persons_films'"},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'p_character': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'p_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person_film_rel'", 'to': "orm['films.Persons']"})
        },
        'robots.kinopoisktries': {
            'Meta': {'object_name': 'KinopoiskTries', 'db_table': "'robots_kinopoisk_tries'"},
            'error_message': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_dump': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'try_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'robots.robots': {
            'Meta': {'object_name': 'Robots', 'db_table': "'robots'"},
            'delay': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'last_start': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'rstatus': ('django.db.models.fields.IntegerField', [], {}),
            'state': ('django.db.models.fields.TextField', [], {})
        },
        'robots.robotslog': {
            'Meta': {'object_name': 'RobotsLog', 'db_table': "'robots_log'"},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itype': ('django.db.models.fields.IntegerField', [], {}),
            'robot_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['robots.Robots']"}),
            'try_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'robots.robotstries': {
            'Meta': {'object_name': 'RobotsTries', 'db_table': "'robots_tries'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'robots_tries'", 'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'outcome': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['robots']