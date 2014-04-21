# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Users'
        db.delete_table('users')

        # Adding model 'Robots'
        db.create_table('robots', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('last_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('next_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('rstatus', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'robots', ['Robots'])

        # Adding model 'RobotsLog'
        db.create_table('robots_log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('robot_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['robots.Robots'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('itype', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'robots', ['RobotsLog'])


    def backwards(self, orm):
        # Deleting model 'Robots'
        db.delete_table('robots')

        # Deleting model 'RobotsLog'
        db.delete_table('robots_log')


    models = {
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