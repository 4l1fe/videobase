# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UsersPics'
        db.create_table('users_pics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pics', to=orm['auth.User'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('users', ['UsersPics'])

        # Adding model 'UsersProfile'
        db.create_table('users_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('last_visited', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('userpic_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('userpic_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ntf_vid_new', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ntf_vid_director', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ntf_frnd_rate', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ntf_frnd_comment', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ntf_frnd_subscribe', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ntf_frequency', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('pvt_subscribes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pvt_friends', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pvt_genres', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pvt_actors', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pvt_directors', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('users', ['UsersProfile'])

        # Adding model 'UsersLogs'
        db.create_table('users_logs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('itype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('iobject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('itext', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('users', ['UsersLogs'])

        # Adding model 'UsersRels'
        db.create_table('users_rels', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rels', to=orm['auth.User'])),
            ('user_rel', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_rel', to=orm['auth.User'])),
            ('rel_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('users', ['UsersRels'])

        # Adding unique constraint on 'UsersRels', fields ['user', 'user_rel']
        db.create_unique('users_rels', ['user_id', 'user_rel_id'])

        # Adding model 'Feed'
        db.create_table('users_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('object', self.gf('jsonfield.fields.JSONField')()),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('users', ['Feed'])

        # Adding model 'UsersSocials'
        db.create_table('users_socials', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('stype', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('stoken', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('suserid', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sphoto', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('users', ['UsersSocials'])

        # Adding model 'SessionToken'
        db.create_table('users_api_session_tokens', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('users', ['SessionToken'])

        # Adding model 'UsersApiSessions'
        db.create_table('users_api_sessions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.SessionToken'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('users', ['UsersApiSessions'])


    def backwards(self, orm):
        # Removing unique constraint on 'UsersRels', fields ['user', 'user_rel']
        db.delete_unique('users_rels', ['user_id', 'user_rel_id'])

        # Deleting model 'UsersPics'
        db.delete_table('users_pics')

        # Deleting model 'UsersProfile'
        db.delete_table('users_profile')

        # Deleting model 'UsersLogs'
        db.delete_table('users_logs')

        # Deleting model 'UsersRels'
        db.delete_table('users_rels')

        # Deleting model 'Feed'
        db.delete_table('users_feed')

        # Deleting model 'UsersSocials'
        db.delete_table('users_socials')

        # Deleting model 'SessionToken'
        db.delete_table('users_api_session_tokens')

        # Deleting model 'UsersApiSessions'
        db.delete_table('users_api_sessions')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'users.feed': {
            'Meta': {'object_name': 'Feed'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object': ('jsonfield.fields.JSONField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'users.sessiontoken': {
            'Meta': {'object_name': 'SessionToken', 'db_table': "'users_api_session_tokens'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'users.usersapisessions': {
            'Meta': {'object_name': 'UsersApiSessions', 'db_table': "'users_api_sessions'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.SessionToken']"})
        },
        'users.userslogs': {
            'Meta': {'object_name': 'UsersLogs', 'db_table': "'users_logs'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iobject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'itext': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'itype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'users.userspics': {
            'Meta': {'object_name': 'UsersPics', 'db_table': "'users_pics'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pics'", 'to': u"orm['auth.User']"})
        },
        'users.usersprofile': {
            'Meta': {'object_name': 'UsersProfile', 'db_table': "'users_profile'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_visited': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ntf_frequency': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'ntf_frnd_comment': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ntf_frnd_rate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ntf_frnd_subscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ntf_vid_director': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ntf_vid_new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pvt_actors': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pvt_directors': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pvt_friends': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pvt_genres': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pvt_subscribes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'userpic_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'userpic_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'users.usersrels': {
            'Meta': {'unique_together': "(('user', 'user_rel'),)", 'object_name': 'UsersRels', 'db_table': "'users_rels'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rel_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rels'", 'to': u"orm['auth.User']"}),
            'user_rel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_rel'", 'to': u"orm['auth.User']"})
        },
        'users.userssocials': {
            'Meta': {'object_name': 'UsersSocials', 'db_table': "'users_socials'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sphoto': ('django.db.models.fields.IntegerField', [], {}),
            'stoken': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'stype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'suserid': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['users']