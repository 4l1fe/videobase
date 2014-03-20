# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'KinopoiskTries.error_message'
        db.add_column('robots_kinopoisk_tries', 'error_message',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'KinopoiskTries.error_message'
        db.delete_column('robots_kinopoisk_tries', 'error_message')


    models = {
        u'films.countries': {
            'Meta': {'object_name': 'Countries', 'db_table': "'countries'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        u'films.genres': {
            'Meta': {'object_name': 'Genres', 'db_table': "'genres'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'robots.kinopoisktries': {
            'Meta': {'object_name': 'KinopoiskTries', 'db_table': "'robots_kinopoisk_tries'"},
            'error_message': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'try_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'robots.robots': {
            'Meta': {'object_name': 'Robots', 'db_table': "'robots'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'last_start': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'next_start': ('django.db.models.fields.DateTimeField', [], {}),
            'rstatus': ('django.db.models.fields.IntegerField', [], {})
        },
        u'robots.robotslog': {
            'Meta': {'object_name': 'RobotsLog', 'db_table': "'robots_log'"},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itype': ('django.db.models.fields.IntegerField', [], {}),
            'robot_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['robots.Robots']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['robots']