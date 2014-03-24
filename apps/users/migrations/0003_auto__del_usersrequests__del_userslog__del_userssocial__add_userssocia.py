# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UsersRequests'
        db.delete_table('users_requests')

        # Deleting model 'UsersLog'
        db.delete_table('users_logs')

        # Deleting model 'UsersSocial'
        db.delete_table('users_socials')

        # Adding model 'UsersSocials'
        db.create_table('users_socials', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'])),
            ('stype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('stoken', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('suserid', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sphoto', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('users', ['UsersSocials'])

        # Adding model 'UsersLogs'
        db.create_table('users_logs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('itype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('iobject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('itext', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('users', ['UsersLogs'])


    def backwards(self, orm):
        # Adding model 'UsersRequests'
        db.create_table('users_requests', (
            ('hash', self.gf('django.db.models.fields.IntegerField')()),
            ('rtype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'users', ['UsersRequests'])

        # Adding model 'UsersLog'
        db.create_table('users_logs', (
            ('itype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('iobject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('itext', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'users', ['UsersLog'])

        # Adding model 'UsersSocial'
        db.create_table('users_socials', (
            ('suserid', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sphoto', self.gf('django.db.models.fields.IntegerField')()),
            ('stoken', self.gf('django.db.models.fields.CharField')(max_length=255)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'])),
        ))
        db.send_create_signal(u'users', ['UsersSocial'])

        # Deleting model 'UsersSocials'
        db.delete_table('users_socials')

        # Deleting model 'UsersLogs'
        db.delete_table('users_logs')


    models = {
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
        'users.userslogs': {
            'Meta': {'object_name': 'UsersLogs', 'db_table': "'users_logs'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iobject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'itext': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'itype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Users']"})
        },
        'users.userspics': {
            'Meta': {'object_name': 'UsersPics', 'db_table': "'users_pics'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Users']"})
        },
        'users.usersrels': {
            'Meta': {'object_name': 'UsersRels', 'db_table': "'users_rels'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Users']"}),
            'user_rel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_rel'", 'to': "orm['users.Users']"})
        },
        'users.userssocials': {
            'Meta': {'object_name': 'UsersSocials', 'db_table': "'users_socials'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sphoto': ('django.db.models.fields.IntegerField', [], {}),
            'stoken': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'stype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'suserid': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Users']"})
        }
    }

    complete_apps = ['users']