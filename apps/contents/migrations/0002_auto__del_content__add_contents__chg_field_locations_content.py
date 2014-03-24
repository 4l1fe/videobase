# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Content'
        db.delete_table('content')

        # Adding model 'Contents'
        db.create_table('content', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['films.Films'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['films.Seasons'], null=True, blank=True)),
            ('viewer_cnt', self.gf('django.db.models.fields.IntegerField')()),
            ('viewer_lastweek_cnt', self.gf('django.db.models.fields.IntegerField')()),
            ('viewer_lastmonth_cnt', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('contents', ['Contents'])


        # Changing field 'Locations.content'
        db.alter_column('locations', 'content_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contents.Contents']))

    def backwards(self, orm):
        # Adding model 'Content'
        db.create_table('content', (
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('viewer_lastmonth_cnt', self.gf('django.db.models.fields.IntegerField')()),
            ('viewer_lastweek_cnt', self.gf('django.db.models.fields.IntegerField')()),
            ('number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['films.Films'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('name_orig', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('viewer_cnt', self.gf('django.db.models.fields.IntegerField')()),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['films.Seasons'], null=True, blank=True)),
        ))
        db.send_create_signal(u'contents', ['Content'])

        # Deleting model 'Contents'
        db.delete_table('content')


        # Changing field 'Locations.content'
        db.alter_column('locations', 'content_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contents.Content']))

    models = {
        'contents.comments': {
            'Meta': {'object_name': 'Comments', 'db_table': "'comments'"},
            'content': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cstatus': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'ctext': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_id': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Users']"})
        },
        'contents.contents': {
            'Meta': {'object_name': 'Contents', 'db_table': "'content'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Seasons']", 'null': 'True', 'blank': 'True'}),
            'viewer_cnt': ('django.db.models.fields.IntegerField', [], {}),
            'viewer_lastmonth_cnt': ('django.db.models.fields.IntegerField', [], {}),
            'viewer_lastweek_cnt': ('django.db.models.fields.IntegerField', [], {})
        },
        'contents.locations': {
            'Meta': {'object_name': 'Locations', 'db_table': "'locations'"},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contents.Contents']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ltype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '30', 'decimal_places': '2'}),
            'price_type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'quality': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'subtitles': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '40'})
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
        'films.seasons': {
            'Meta': {'unique_together': "(('film', 'number'),)", 'object_name': 'Seasons', 'db_table': "'seasons'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'series_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
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

    complete_apps = ['contents']