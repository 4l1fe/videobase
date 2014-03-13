# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('users', 'passhash', 'password')

    def backwards(self, orm):
        db.rename_column('users', 'password', 'passhash')

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