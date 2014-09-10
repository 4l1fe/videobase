# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'UsersCasts.subscribed'
        db.alter_column('users_casts', 'subscribed', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'UsersCasts.subscribed'
        db.alter_column('users_casts', 'subscribed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 9, 2, 0, 0)))

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
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'casts'", 'symmetrical': 'False', 'to': "orm['casts.AbstractCastsTags']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'title_orig': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'casts.castschats': {
            'Meta': {'object_name': 'CastsChats', 'db_table': "'casts_chats'"},
            'cast': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['casts.Casts']", 'unique': 'True'}),
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
        'casts.castsextras': {
            'Meta': {'object_name': 'CastsExtras', 'db_table': "'extras_casts'"},
            'cast': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['casts.Casts']"}),
            'extra': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.FilmExtras']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        'casts.userscasts': {
            'Meta': {'object_name': 'UsersCasts', 'db_table': "'users_casts'"},
            'cast': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['casts.Casts']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'subscribed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'films.cities': {
            'Meta': {'object_name': 'Cities', 'db_table': "'cities'"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'to': "orm['films.Countries']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'films.countries': {
            'Meta': {'object_name': 'Countries', 'db_table': "'countries'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'films.filmextras': {
            'Meta': {'object_name': 'FilmExtras', 'db_table': "'films_extras'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fe_film_rel'", 'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'films.films': {
            'Meta': {'object_name': 'Films', 'db_table': "'films'"},
            'age_limit': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'budget': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'countries'", 'symmetrical': 'False', 'to': "orm['films.Countries']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'genres'", 'symmetrical': 'False', 'to': "orm['films.Genres']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'kinopoisk_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'kinopoisk_lastupdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            'persons': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'persons'", 'symmetrical': 'False', 'through': "orm['films.PersonsFilms']", 'to': "orm['films.Persons']"}),
            'rating_cons': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'rating_cons_cnt': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'rating_imdb': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'rating_imdb_cnt': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'rating_kinopoisk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rating_kinopoisk_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating_local': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'rating_local_cnt': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'rating_sort': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'seasons_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'was_shown': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'films.genres': {
            'Meta': {'object_name': 'Genres', 'db_table': "'genres'"},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'hidden': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'rgt': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'films.persons': {
            'Meta': {'object_name': 'Persons', 'db_table': "'persons'"},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'persons'", 'null': 'True', 'to': "orm['films.Cities']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kinopoisk_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'name_orig': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'films.personsfilms': {
            'Meta': {'unique_together': "(('film', 'person', 'p_type'),)", 'object_name': 'PersonsFilms', 'db_table': "'persons_films'"},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pf_films_rel'", 'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'p_character': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'p_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'p_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pf_persons_rel'", 'to': "orm['films.Persons']"})
        }
    }

    complete_apps = ['casts']