# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AbstractCastsTags'
        db.create_table('abstract_casts_tags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=255, db_index=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
        ))
        db.send_create_signal('casts', ['AbstractCastsTags'])

        # Adding model 'Casts'
        db.create_table('casts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('title_orig', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=255, db_index=True)),
            ('pg_rating', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('casts', ['Casts'])

        # Adding M2M table for field tags on 'Casts'
        m2m_table_name = db.shorten_name('casts_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('casts', models.ForeignKey(orm['casts.casts'], null=False)),
            ('abstractcaststags', models.ForeignKey(orm['casts.abstractcaststags'], null=False))
        ))
        db.create_unique(m2m_table_name, ['casts_id', 'abstractcaststags_id'])

        # Adding model 'CastsChats'
        db.create_table('casts_chats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['casts.Casts'])),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('casts', ['CastsChats'])

        # Adding model 'CastsChatsUsers'
        db.create_table('casts_chats_users', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['casts.Casts'])),
            ('blocked', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
        ))
        db.send_create_signal('casts', ['CastsChatsUsers'])

        # Adding model 'CastsChatsMsgs'
        db.create_table('casts_chats_msgs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['casts.Casts'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('casts', ['CastsChatsMsgs'])

        # Adding model 'CastsLocations'
        db.create_table('casts_locations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cast_service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['casts.CastsServices'])),
            ('cast', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cl_location_rel', to=orm['casts.Casts'])),
            ('quality', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
            ('price_type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('offline', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('url_view', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
            ('value', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
        ))
        db.send_create_signal('casts', ['CastsLocations'])

        # Adding model 'CastsServices'
        db.create_table('casts_services', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=255, db_index=True)),
            ('update', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('casts', ['CastsServices'])

        # Adding M2M table for field tags on 'CastsServices'
        m2m_table_name = db.shorten_name('casts_services_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('castsservices', models.ForeignKey(orm['casts.castsservices'], null=False)),
            ('abstractcaststags', models.ForeignKey(orm['casts.abstractcaststags'], null=False))
        ))
        db.create_unique(m2m_table_name, ['castsservices_id', 'abstractcaststags_id'])

        # Adding model 'ExtrasCasts'
        db.create_table('extras_casts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['casts.Casts'])),
            ('extra', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('casts', ['ExtrasCasts'])

        # Adding model 'UsersCasts'
        db.create_table('users_casts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['casts.Casts'])),
            ('rating', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, null=True, blank=True)),
            ('subscribed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('casts', ['UsersCasts'])


    def backwards(self, orm):
        # Deleting model 'AbstractCastsTags'
        db.delete_table('abstract_casts_tags')

        # Deleting model 'Casts'
        db.delete_table('casts')

        # Removing M2M table for field tags on 'Casts'
        db.delete_table(db.shorten_name('casts_tags'))

        # Deleting model 'CastsChats'
        db.delete_table('casts_chats')

        # Deleting model 'CastsChatsUsers'
        db.delete_table('casts_chats_users')

        # Deleting model 'CastsChatsMsgs'
        db.delete_table('casts_chats_msgs')

        # Deleting model 'CastsLocations'
        db.delete_table('casts_locations')

        # Deleting model 'CastsServices'
        db.delete_table('casts_services')

        # Removing M2M table for field tags on 'CastsServices'
        db.delete_table(db.shorten_name('casts_services_tags'))

        # Deleting model 'ExtrasCasts'
        db.delete_table('extras_casts')

        # Deleting model 'UsersCasts'
        db.delete_table('users_casts')


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
        'casts.abstractcaststags': {
            'Meta': {'object_name': 'AbstractCastsTags', 'db_table': "'abstract_casts_tags'"},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'})
        },
        'casts.casts': {
            'Meta': {'object_name': 'Casts', 'db_table': "'casts'"},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'db_index': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pg_rating': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'casts'", 'symmetrical': 'False', 'to': "orm['casts.AbstractCastsTags']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'title_orig': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'casts.castschats': {
            'Meta': {'object_name': 'CastsChats', 'db_table': "'casts_chats'"},
            'cast': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['casts.Casts']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {})
        },
        'casts.castschatsmsgs': {
            'Meta': {'object_name': 'CastsChatsMsgs', 'db_table': "'casts_chats_msgs'"},
            'cast': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['casts.Casts']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'casts.castschatsusers': {
            'Meta': {'object_name': 'CastsChatsUsers', 'db_table': "'casts_chats_users'"},
            'blocked': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cast': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['casts.Casts']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'casts.castslocations': {
            'Meta': {'object_name': 'CastsLocations', 'db_table': "'casts_locations'"},
            'cast': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cl_location_rel'", 'to': "orm['casts.Casts']"}),
            'cast_service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['casts.CastsServices']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offline': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'price_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'quality': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'url_view': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'})
        },
        'casts.castsservices': {
            'Meta': {'object_name': 'CastsServices', 'db_table': "'casts_services'"},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'casts_services'", 'symmetrical': 'False', 'to': "orm['casts.AbstractCastsTags']"}),
            'update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'})
        },
        'casts.extrascasts': {
            'Meta': {'object_name': 'ExtrasCasts', 'db_table': "'extras_casts'"},
            'cast': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['casts.Casts']"}),
            'extra': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'casts.userscasts': {
            'Meta': {'object_name': 'UsersCasts', 'db_table': "'users_casts'"},
            'cast': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['casts.Casts']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'subscribed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['casts']