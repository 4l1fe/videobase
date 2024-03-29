# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cities'
        db.create_table('cities', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cities', to=orm['films.Countries'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('films', ['Cities'])

        # Adding model 'Countries'
        db.create_table('countries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('films', ['Countries'])

        # Adding model 'Genres'
        db.create_table('genres', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rgt', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('rating_sort', self.gf('django.db.models.fields.SmallIntegerField')(db_index=True, null=True, blank=True)),
        ))
        db.send_create_signal('films', ['Genres'])

        # Adding model 'Seasons'
        db.create_table('seasons', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['films.Films'])),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('series_cnt', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('films', ['Seasons'])

        # Adding unique constraint on 'Seasons', fields ['film', 'number']
        db.create_unique('seasons', ['film_id', 'number'])

        # Adding model 'Films'
        db.create_table('films', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('release_date', self.gf('django.db.models.fields.DateField')(db_index=True, null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('budget', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('rating_local', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('rating_local_cnt', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('imdb_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rating_imdb', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('rating_imdb_cnt', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('rating_cons', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('rating_cons_cnt', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('rating_sort', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, db_index=True, blank=True)),
            ('kinopoisk_id', self.gf('django.db.models.fields.IntegerField')(unique=True, db_index=True)),
            ('age_limit', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, null=True, blank=True)),
            ('kinopoisk_lastupdate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('rating_kinopoisk', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('rating_kinopoisk_cnt', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('seasons_cnt', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(default='', max_length=255, db_index=True, blank=True)),
            ('search_index', self.gf('djorm_pgfulltext.fields.VectorField')(default='', null=True, db_index=True)),
        ))
        db.send_create_signal('films', ['Films'])

        # Adding M2M table for field countries on 'Films'
        m2m_table_name = db.shorten_name('films_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('films', models.ForeignKey(orm['films.films'], null=False)),
            ('countries', models.ForeignKey(orm['films.countries'], null=False))
        ))
        db.create_unique(m2m_table_name, ['films_id', 'countries_id'])

        # Adding M2M table for field genres on 'Films'
        m2m_table_name = db.shorten_name('films_genres')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('films', models.ForeignKey(orm['films.films'], null=False)),
            ('genres', models.ForeignKey(orm['films.genres'], null=False))
        ))
        db.create_unique(m2m_table_name, ['films_id', 'genres_id'])

        # Adding model 'FilmExtras'
        db.create_table('films_extras', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fe_film_rel', to=orm['films.Films'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('films', ['FilmExtras'])

        # Adding model 'Persons'
        db.create_table('persons', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='persons', null=True, to=orm['films.Cities'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('name_orig', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('bio', self.gf('django.db.models.fields.TextField')()),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('kinopoisk_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
        ))
        db.send_create_signal('films', ['Persons'])

        # Adding model 'PersonsExtras'
        db.create_table('persons_extras', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['films.Persons'], max_length=255)),
            ('etype', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('name_orig', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('films', ['PersonsExtras'])

        # Adding model 'PersonsFilms'
        db.create_table('persons_films', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pf_films_rel', to=orm['films.Films'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pf_persons_rel', to=orm['films.Persons'])),
            ('p_type', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('p_character', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('films', ['PersonsFilms'])

        # Adding unique constraint on 'PersonsFilms', fields ['film', 'person', 'p_type']
        db.create_unique('persons_films', ['film_id', 'person_id', 'p_type'])

        # Adding model 'UsersFilms'
        db.create_table('users_films', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='uf_users_rel', to=orm['auth.User'])),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(related_name='uf_films_rel', to=orm['films.Films'])),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, null=True, db_index=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, null=True, blank=True)),
            ('subscribed', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('films', ['UsersFilms'])

        # Adding unique constraint on 'UsersFilms', fields ['user', 'film']
        db.create_unique('users_films', ['user_id', 'film_id'])

        # Adding model 'UsersPersons'
        db.create_table('users_persons', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='up_users_rel', max_length=255, to=orm['auth.User'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='up_persons_rel', max_length=255, to=orm['films.Persons'])),
            ('upstatus', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('subscribed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('films', ['UsersPersons'])

        # Adding model 'YoutubeTrailerCheck'
        db.create_table('youtube_trailer_check', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('film', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['films.Films'])),
            ('last_check', self.gf('django.db.models.fields.DateTimeField')()),
            ('was_successfull', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('films', ['YoutubeTrailerCheck'])


    def backwards(self, orm):
        # Removing unique constraint on 'UsersFilms', fields ['user', 'film']
        db.delete_unique('users_films', ['user_id', 'film_id'])

        # Removing unique constraint on 'PersonsFilms', fields ['film', 'person', 'p_type']
        db.delete_unique('persons_films', ['film_id', 'person_id', 'p_type'])

        # Removing unique constraint on 'Seasons', fields ['film', 'number']
        db.delete_unique('seasons', ['film_id', 'number'])

        # Deleting model 'Cities'
        db.delete_table('cities')

        # Deleting model 'Countries'
        db.delete_table('countries')

        # Deleting model 'Genres'
        db.delete_table('genres')

        # Deleting model 'Seasons'
        db.delete_table('seasons')

        # Deleting model 'Films'
        db.delete_table('films')

        # Removing M2M table for field countries on 'Films'
        db.delete_table(db.shorten_name('films_countries'))

        # Removing M2M table for field genres on 'Films'
        db.delete_table(db.shorten_name('films_genres'))

        # Deleting model 'FilmExtras'
        db.delete_table('films_extras')

        # Deleting model 'Persons'
        db.delete_table('persons')

        # Deleting model 'PersonsExtras'
        db.delete_table('persons_extras')

        # Deleting model 'PersonsFilms'
        db.delete_table('persons_films')

        # Deleting model 'UsersFilms'
        db.delete_table('users_films')

        # Deleting model 'UsersPersons'
        db.delete_table('users_persons')

        # Deleting model 'YoutubeTrailerCheck'
        db.delete_table('youtube_trailer_check')


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
            'rating_cons_cnt': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'rating_imdb': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'rating_imdb_cnt': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'rating_kinopoisk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rating_kinopoisk_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating_local': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'rating_local_cnt': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'rating_sort': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'seasons_cnt': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'films.genres': {
            'Meta': {'object_name': 'Genres', 'db_table': "'genres'"},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'rating_sort': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
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
        'films.personsextras': {
            'Meta': {'object_name': 'PersonsExtras', 'db_table': "'persons_extras'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'etype': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'name_orig': ('django.db.models.fields.TextField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Persons']", 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'films.personsfilms': {
            'Meta': {'unique_together': "(('film', 'person', 'p_type'),)", 'object_name': 'PersonsFilms', 'db_table': "'persons_films'"},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pf_films_rel'", 'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'p_character': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'p_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pf_persons_rel'", 'to': "orm['films.Persons']"})
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
        'films.usersfilms': {
            'Meta': {'unique_together': "(('user', 'film'),)", 'object_name': 'UsersFilms', 'db_table': "'users_films'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'film': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'uf_films_rel'", 'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'subscribed': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'uf_users_rel'", 'to': u"orm['auth.User']"})
        },
        'films.userspersons': {
            'Meta': {'object_name': 'UsersPersons', 'db_table': "'users_persons'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'up_persons_rel'", 'max_length': '255', 'to': "orm['films.Persons']"}),
            'subscribed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'upstatus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'up_users_rel'", 'max_length': '255', 'to': u"orm['auth.User']"})
        },
        'films.youtubetrailercheck': {
            'Meta': {'object_name': 'YoutubeTrailerCheck', 'db_table': "'youtube_trailer_check'"},
            'film': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['films.Films']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_check': ('django.db.models.fields.DateTimeField', [], {}),
            'was_successfull': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['films']