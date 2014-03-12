# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Users'
        db.create_table('users', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('passhash', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_visited', self.gf('django.db.models.fields.DateTimeField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ustatus', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('userpic_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('userpic', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['users.UsersPics'], null=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['Users'])

        # Adding model 'UsersRequests'
        db.create_table('users_requests', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'])),
            ('hash', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('rtype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'users', ['UsersRequests'])

        # Adding model 'UsersLog'
        db.create_table('users_logs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('itype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('iobject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('itext', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'users', ['UsersLog'])

        # Adding model 'UsersPics'
        db.create_table('users_pics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'users', ['UsersPics'])

        # Adding model 'UsersSocial'
        db.create_table('users_socials', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'])),
            ('stype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('stoken', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('suserid', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sphoto', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'users', ['UsersSocial'])

        # Adding model 'Persons'
        db.create_table('persons', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bio', self.gf('django.db.models.fields.TextField')()),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['Persons'])

        # Adding model 'PersonsExtras'
        db.create_table('persons_extras', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Persons'], max_length=255)),
            ('etype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('name_orig', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'users', ['PersonsExtras'])

        # Adding model 'UsersPersons'
        db.create_table('users_persons', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Users'], max_length=255)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Persons'], max_length=255)),
            ('upstatus', self.gf('django.db.models.fields.IntegerField')()),
            ('subscribed', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'users', ['UsersPersons'])


    def backwards(self, orm):
        # Deleting model 'Users'
        db.delete_table('users')

        # Deleting model 'UsersRequests'
        db.delete_table('users_requests')

        # Deleting model 'UsersLog'
        db.delete_table('users_logs')

        # Deleting model 'UsersPics'
        db.delete_table('users_pics')

        # Deleting model 'UsersSocial'
        db.delete_table('users_socials')

        # Deleting model 'Persons'
        db.delete_table('persons')

        # Deleting model 'PersonsExtras'
        db.delete_table('persons_extras')

        # Deleting model 'UsersPersons'
        db.delete_table('users_persons')


    models = {
        u'users.persons': {
            'Meta': {'object_name': 'Persons', 'db_table': "'persons'"},
            'bio': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'users.personsextras': {
            'Meta': {'object_name': 'PersonsExtras', 'db_table': "'persons_extras'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'etype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'name_orig': ('django.db.models.fields.TextField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Persons']", 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        u'users.userspersons': {
            'Meta': {'object_name': 'UsersPersons', 'db_table': "'users_persons'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Persons']", 'max_length': '255'}),
            'subscribed': ('django.db.models.fields.IntegerField', [], {}),
            'upstatus': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Users']", 'max_length': '255'})
        },
        u'users.userspics': {
            'Meta': {'object_name': 'UsersPics', 'db_table': "'users_pics'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Users']"})
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
