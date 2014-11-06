# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.common
import djorm_pgfulltext.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractCastsTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', db_index=True, blank=True)),
                ('name_orig', models.CharField(default=b'', max_length=255, verbose_name='\u041e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0435 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', db_index=True, blank=True)),
                ('description', models.TextField(max_length=255, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', db_index=True)),
                ('type', models.CharField(default=b'', max_length=255, verbose_name='\u0422\u0438\u043f', db_index=True, blank=True)),
            ],
            options={
                'db_table': 'abstract_casts_tags',
                'verbose_name': '\u0422\u0435\u0433 \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438',
                'verbose_name_plural': '\u0422\u0435\u0433\u0438 \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CastExtrasStorage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('name_orig', models.CharField(max_length=255, verbose_name='\u041e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0435 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('photo', models.ImageField(upload_to=utils.common.get_image_path, null=True, verbose_name='\u041f\u043e\u0441\u0442\u0435\u0440', blank=True)),
            ],
            options={
                'db_table': 'casts_extras',
                'verbose_name': '\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b \u043a cast',
                'verbose_name_plural': '\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u044b \u043a cast',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Casts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438', db_index=True)),
                ('title_orig', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u0430', db_index=True)),
                ('start', models.DateTimeField(verbose_name='\u0412\u0440\u0435\u043c\u044f \u043d\u0430\u0447\u0430\u043b\u0430 \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438')),
                ('duration', models.IntegerField(null=True, verbose_name='\u041f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c', blank=True)),
                ('status', models.CharField(db_index=True, max_length=255, null=True, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', blank=True)),
                ('description', models.TextField(max_length=255, null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('pg_rating', models.CharField(max_length=255, null=True, verbose_name='\u0412\u043e\u0437\u0440\u0430\u0441\u0442\u043d\u043e\u0439 \u0440\u0435\u0439\u0442\u0438\u043d\u0433', blank=True)),
                ('search_index', djorm_pgfulltext.fields.VectorField(default=b'', serialize=False, null=True, editable=False, db_index=True)),
                ('tags', models.ManyToManyField(related_name='casts', verbose_name='Tags', to='casts.AbstractCastsTags')),
            ],
            options={
                'db_table': 'casts',
                'verbose_name': '\u0422\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u044f',
                'verbose_name_plural': '\u0422\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CastsChats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441')),
                ('cast', models.OneToOneField(verbose_name='\u0422\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u044f', to='casts.Casts')),
            ],
            options={
                'db_table': 'casts_chats',
                'verbose_name': '\u0427\u0430\u0442 \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438 ',
                'verbose_name_plural': '\u0427\u0430\u0442\u044b \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CastsChatsMsgs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0421\u043e\u0437\u0434\u0430\u043d')),
                ('text', models.TextField(null=True, verbose_name='\u041a\u043e\u0434 \u0432\u0441\u0442\u0440\u0430\u0438\u0432\u0430\u043d\u0438\u044f', blank=True)),
                ('cast', models.ForeignKey(verbose_name='\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043b\u044f', to='casts.Casts')),
                ('user', models.ForeignKey(verbose_name='\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043b\u044f', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'casts_chats_msgs',
                'verbose_name': '\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 \u0432 \u0447\u0430\u0442\u0435 \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438',
                'verbose_name_plural': '\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f \u0432 \u0447\u0430\u0442\u0430\u0445 \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CastsChatsUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('blocked', models.DateTimeField(auto_now_add=True, verbose_name='\u0412\u0440\u0435\u043c\u044f \u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u043a\u0438')),
                ('status', models.CharField(default=b'', max_length=255, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', db_index=True, blank=True)),
                ('cast', models.ForeignKey(verbose_name='\u0422\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u044f', to='casts.Casts')),
                ('user', models.ForeignKey(verbose_name='\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043b\u044f', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'casts_chats_users',
                'verbose_name': '\u0427\u0430\u0442 \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u0427\u0430\u0442\u044b \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0439 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CastsExtras',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cast', models.ForeignKey(verbose_name='\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043b\u044f', to='casts.Casts')),
                ('extra', models.ForeignKey(verbose_name='Extra', to='casts.CastExtrasStorage')),
            ],
            options={
                'db_table': 'extras_casts',
                'verbose_name': '\u0422\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438 extra',
                'verbose_name_plural': '\u0422\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438 extra',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CastsLocations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quality', models.CharField(default=b'', max_length=255, verbose_name='\u041a\u0430\u0447\u0435\u0441\u0442\u0432\u043e', db_index=True, blank=True)),
                ('price_type', models.IntegerField(blank=True, null=True, verbose_name='\u0422\u0438\u043f \u0446\u0435\u043d\u044b', db_index=True, choices=[(0, b'\xd0\x91\xd0\xb5\xd1\x81\xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd0\xbd\xd0\xbe'), (2, b'\xd0\x9f\xd0\xbb\xd0\xb0\xd1\x82\xd0\xbd\xd0\xbe')])),
                ('price', models.FloatField(default=0, null=True, verbose_name='\u0426\u0435\u043d\u0430')),
                ('offline', models.BooleanField(default=True, verbose_name='\u041e\u0444\u0444\u043b\u0430\u0439\u043d ?')),
                ('url_view', models.CharField(default=b'', max_length=255, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430', db_index=True, blank=True)),
                ('value', models.CharField(default=b'', max_length=255, verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435', db_index=True, blank=True)),
                ('cast', models.ForeignKey(related_name='cl_location_rel', verbose_name='\u0422\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u044f', to='casts.Casts')),
            ],
            options={
                'db_table': 'casts_locations',
                'verbose_name': '\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u044e',
                'verbose_name_plural': '\u0421\u0441\u044b\u043b\u043a\u0438 \u043d\u0430 \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CastsServices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', db_index=True)),
                ('url', models.CharField(default=b'', max_length=255, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430', db_index=True, blank=True)),
                ('description', models.TextField(max_length=255, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', db_index=True)),
                ('update', models.DateTimeField(null=True, verbose_name='\u0412\u0440\u0435\u043c\u044f \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f', blank=True)),
                ('tags', models.ManyToManyField(related_name='casts_services', verbose_name='\u0422\u0435\u0433\u0438', to='casts.AbstractCastsTags')),
            ],
            options={
                'db_table': 'casts_services',
                'verbose_name': '\u0421\u0435\u0440\u0432\u0438\u0441 \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0439',
                'verbose_name_plural': '\u0421\u0435\u0440\u0432\u0438\u0441\u044b \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersCasts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.PositiveSmallIntegerField(db_index=True, null=True, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433 \u043f\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043d\u044b\u0439 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u043c', blank=True)),
                ('subscribed', models.DateTimeField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', blank=True)),
                ('cast', models.ForeignKey(verbose_name='\u0422\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u044f', to='casts.Casts')),
                ('user', models.ForeignKey(verbose_name='\u0418\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u043e\u0440 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043b\u044f', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users_casts',
                'verbose_name': '\u0422\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u0422\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='userscasts',
            unique_together=set([('user', 'cast')]),
        ),
        migrations.AddField(
            model_name='castslocations',
            name='cast_service',
            field=models.ForeignKey(verbose_name='\u0421\u0435\u0440\u0432\u0438\u0441 \u0442\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0439', to='casts.CastsServices'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='castextrasstorage',
            name='cast',
            field=models.ForeignKey(related_name='ce_cast_rel', verbose_name='Cast', to='casts.Casts'),
            preserve_default=True,
        ),
    ]
