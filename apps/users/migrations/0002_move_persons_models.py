# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Persons'
        db.delete_table('persons')

        # Deleting model 'PersonsExtras'
        db.delete_table('persons_extras')

        # Deleting model 'UsersPersons'
        db.delete_table('users_persons')


    def backwards(self, orm):
        # Adding model 'Persons'
        db.create_table('persons', (
            ('bio', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(max_length=255)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'users', ['Persons'])

        # Adding model 'PersonsExtras'
        db.create_table('persons_extras', (
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Persons'], max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('etype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_orig', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'users', ['PersonsExtras'])

        # Adding model 'UsersPersons'
        db.create_table('users_persons', (
            ('upstatus', self.gf('django.db.models.fields.IntegerField')()),
            ('subscribed', self.gf('django.db.models.fields.IntegerField')()),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Persons'], max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'], max_length=255)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'users', ['UsersPersons'])


    models = {
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
        u'users.userslog': {
            'Meta': {'object_name': 'UsersLog', 'db_table': "'users_logs'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iobject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'itext': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'itype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Users']"})
        },
        u'users.userspics': {
            'Meta': {'object_name': 'UsersPics', 'db_table': "'users_pics'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Users']"})
        },
        u'users.usersrels': {
            'Meta': {'object_name': 'UsersRels', 'db_table': "'users_rels'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Users']"}),
            'user_rel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_rel'", 'to': u"orm['users.Users']"})
        },
        u'users.usersrequests': {
            'Meta': {'object_name': 'UsersRequests', 'db_table': "'users_requests'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hash': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rtype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Users']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'users.userssocial': {
            'Meta': {'object_name': 'UsersSocial', 'db_table': "'users_socials'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sphoto': ('django.db.models.fields.IntegerField', [], {}),
            'stoken': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'stype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'suserid': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Users']"})
        }
    }

    complete_apps = ['users']