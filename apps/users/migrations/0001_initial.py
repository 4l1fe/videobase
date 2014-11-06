# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import utils.common


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd1\x81\xd0\xbe\xd0\xb7\xd0\xb4\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('type', models.CharField(max_length=255, verbose_name=b'\xd0\xa2\xd0\xb8\xd0\xbf \xd1\x81\xd0\xb2\xd1\x8f\xd0\xb7\xd0\xb0\xd0\xbd\xd0\xbd\xd0\xbe\xd0\xb3\xd0\xbe \xd0\xbe\xd0\xb1\xd1\x8a\xd0\xb5\xd0\xba\xd1\x82\xd0\xb0', choices=[(b'film-r', '\u041e\u0446\u0435\u043d\u043a\u0430 \u0444\u0438\u043b\u044c\u043c\u0430'), (b'film-s', '\u041f\u043e\u0434\u043f\u0438\u0441\u043a\u0430 \u043d\u0430 \u0444\u0438\u043b\u044c\u043c'), (b'film-nw', "\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d \u043f\u0440\u0438\u0437\u043d\u0430\u043a '\u043d\u0435 \u0441\u043c\u043e\u0442\u0440\u0435\u0442\u044c'"), (b'film-c', '\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u043a \u0444\u0438\u043b\u044c\u043c\u0443'), (b'film-o', '\u0424\u0438\u043b\u044c\u043c \u043f\u043e\u044f\u0432\u0438\u043b\u0441\u044f \u0432 \u043a\u0438\u043d\u043e\u0442\u0435\u0430\u0442\u0440\u0435'), (b'pers-s', '\u041f\u043e\u0434\u043f\u0438\u0441\u043a\u0430 \u043d\u0430 \u043f\u0435\u0440\u0441\u043e\u043d\u0443'), (b'pers-o', '\u041f\u043e\u044f\u0432\u043b\u0435\u043d\u0438\u0435 \u0444\u0438\u043b\u044c\u043c\u0430 \u0441 \u0443\u0447\u0430\u0441\u0442\u0438\u0435\u043c \u043f\u0435\u0440\u0441\u043e\u043d\u044b'), (b'user-a', '\u041f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u0434\u0440\u0443\u0436\u0438\u0442\u044c'), (b'user-f', '\u042e\u0437\u0435\u0440\u044b \u0434\u0440\u0443\u0437\u044c\u044f'), (b'sys-a', '\u0421\u0438\u0441\u0442\u0435\u043c\u043d\u043e\u0435 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435')])),
                ('obj_id', models.IntegerField(null=True, verbose_name=b'\xd0\x98\xd0\xb4\xd0\xb5\xd0\xbd\xd1\x82\xd0\xb8\xd1\x84\xd0\xb8\xd0\xba\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80 \xd0\xbe\xd0\xb1\xd1\x8a\xd0\xb5\xd0\xba\xd1\x82\xd0\xb0', blank=True)),
                ('child_obj_id', models.IntegerField(null=True, verbose_name=b'\xd0\x98\xd0\xb4\xd0\xb5\xd0\xbd\xd1\x82\xd0\xb8\xd1\x84\xd0\xb8\xd0\xba\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80 \xd0\xb4\xd0\xbe\xd1\x87\xd0\xb5\xd1\x80\xd0\xbd\xd0\xb5\xd0\xb3\xd0\xbe \xd0\xbe\xd0\xb1\xd1\x8a\xd0\xb5\xd0\xba\xd1\x82\xd0\xb0', blank=True)),
                ('text', models.TextField(null=True, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xba\xd1\x81\xd1\x82', blank=True)),
                ('user', models.ForeignKey(verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xb7\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'users_feed',
                'verbose_name': '\u041b\u0435\u043d\u0442\u0430 \u0441\u043e\u0431\u044b\u0442\u0438\u0439',
                'verbose_name_plural': '\u041b\u0435\u043d\u0442\u044b \u0441\u043e\u0431\u044b\u0442\u0438\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SessionToken',
            fields=[
                ('key', models.CharField(max_length=40, serialize=False, verbose_name='\u0422\u043e\u043a\u0435\u043d', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='\u0412\u0440\u0435\u043c\u044f \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u044c \u0441\u044d\u0441\u0441\u0438\u0438')),
                ('user', models.ForeignKey(related_name='session', verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('updated',),
                'db_table': 'session_token',
                'verbose_name': '\u0422\u043e\u043a\u0435\u043d \u0441\u0435\u0441\u0441\u0438\u0438',
                'verbose_name_plural': '\u0422\u043e\u043a\u0435\u043d\u044b \u0441\u0435\u0441\u0441\u0438\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersHash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash_key', models.CharField(verbose_name='\u0425\u0435\u0448', unique=True, max_length=255, editable=False)),
                ('hash_type', models.CharField(verbose_name='\u0425\u0435\u0448 \u0442\u0438\u043f', max_length=255, editable=False, choices=[(1, '\u0421\u043c\u0435\u043d\u0430 email'), (2, '\u0421\u043c\u0435\u043d\u0430 \u043f\u0430\u0440\u043e\u043b\u044f'), (3, '\u041f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438')])),
                ('created', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('expired', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0438\u0441\u0442\u0435\u0447\u0435\u043d\u0438\u044f', editable=False)),
                ('user', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users_hash',
                'verbose_name': '\u0425\u0435\u0448 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u0425\u0435\u0448\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersLogs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('itype', models.CharField(max_length=255, verbose_name='\u0422\u0438\u043f')),
                ('iobject', models.CharField(max_length=255, verbose_name='\u041e\u0431\u044a\u0435\u043a\u0442')),
                ('itext', models.CharField(max_length=255, verbose_name='\u0422\u0435\u043a\u0441\u0442')),
                ('user', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users_logs',
                'verbose_name': '\u041b\u043e\u0433 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u041b\u043e\u0433\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersPics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'local', max_length=255, verbose_name='\u0422\u0438\u043f', choices=[(b'vk-oauth2', b'Vkontakte'), (b'facebook', b'Facebook'), (b'twitter', b'Twitter'), (b'google-oauth2', b'Google+'), (b'local', b'\xd0\x98\xd0\xb7 \xd1\x81\xd0\xbe\xd0\xb1\xd1\x81\xd1\x82\xd0\xb2\xd0\xb5\xd0\xbd\xd0\xbd\xd1\x8b\xd1\x85 \xd0\xb7\xd0\xb0\xd0\xb3\xd1\x80\xd1\x83\xd0\xb7\xd0\xbe\xd0\xba')])),
                ('image', models.ImageField(upload_to=utils.common.get_image_path, verbose_name='\u0410\u0432\u0430\u0442\u0430\u0440\u043a\u0430')),
                ('user', models.ForeignKey(related_name='pics', verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users_pics',
                'verbose_name': '\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u041a\u0430\u0440\u0442\u0438\u043d\u043a\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_visited', models.DateTimeField(auto_now_add=True, verbose_name='\u041f\u0435\u0441\u043b\u0435\u0434\u043d\u0438\u0439 \u0432\u0438\u0437\u0438\u0442')),
                ('userpic_id', models.IntegerField(null=True, verbose_name='Id \u0430\u0432\u0430\u0442\u0430\u0440\u043a\u0438', blank=True)),
                ('ntf_vid_new', models.BooleanField(default=True, verbose_name='\u041f\u043e\u044f\u0432\u043b\u0435\u043d\u0438\u0435 \u043d\u043e\u0432\u043e\u0433\u043e \u0444\u0438\u043b\u044c\u043c\u0430')),
                ('ntf_vid_director', models.BooleanField(default=True, verbose_name='\u041f\u043e\u044f\u0432\u043b\u0435\u043d\u0438\u0435 \u0444\u0438\u043b\u044c\u043c\u0430 \u0441 \u043f\u0435\u0440\u0441\u043e\u043d\u043e\u0439')),
                ('ntf_frnd_rate', models.BooleanField(default=True, verbose_name='\u041d\u043e\u0432\u0430\u044f \u043e\u0446\u0435\u043d\u043a\u0430 \u0434\u0440\u0443\u0437\u0435\u0439')),
                ('ntf_frnd_comment', models.BooleanField(default=True, verbose_name='\u041d\u043e\u0432\u044b\u0439 \u043a\u043e\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439 \u0434\u0440\u0443\u0437\u0435\u0439')),
                ('ntf_frnd_subscribe', models.BooleanField(default=True, verbose_name='\u041d\u043e\u0432\u0430\u044f \u043f\u043e\u0434\u043f\u0438\u0441\u043a\u0430 \u0434\u0440\u0443\u0437\u0435\u0439')),
                ('ntf_frequency', models.IntegerField(default=1, verbose_name='\u0427\u0430\u0441\u0442\u043e\u0442\u0430 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0439', choices=[(1, '\u041e\u0434\u0438\u043d \u0440\u0430\u0437 \u0432 \u0434\u0435\u043d\u044c'), (7, '\u0420\u0430\u0437 \u0432 \u043d\u0435\u0434\u0435\u043b\u044e'), (0, '\u041d\u0438\u043a\u043e\u0433\u0434\u0430')])),
                ('pvt_subscribes', models.IntegerField(default=0, verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u043a\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', choices=[(0, '\u0412\u0438\u0434\u043d\u043e \u0432\u0441\u0435\u043c'), (1, '\u0412\u0438\u0434\u043d\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u0434\u0440\u0443\u0437\u044c\u044f\u043c'), (2, '\u0412\u0438\u0434\u043d\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u043c\u043d\u0435')])),
                ('pvt_friends', models.IntegerField(default=0, verbose_name='\u0414\u0440\u0443\u0437\u044c\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', choices=[(0, '\u0412\u0438\u0434\u043d\u043e \u0432\u0441\u0435\u043c'), (1, '\u0412\u0438\u0434\u043d\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u0434\u0440\u0443\u0437\u044c\u044f\u043c'), (2, '\u0412\u0438\u0434\u043d\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u043c\u043d\u0435')])),
                ('pvt_genres', models.IntegerField(default=0, verbose_name='\u041b\u044e\u0431\u0438\u043c\u044b\u0435 \u0436\u0430\u043d\u0440\u044b \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', choices=[(0, '\u0412\u0438\u0434\u043d\u043e \u0432\u0441\u0435\u043c'), (1, '\u0412\u0438\u0434\u043d\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u0434\u0440\u0443\u0437\u044c\u044f\u043c'), (2, '\u0412\u0438\u0434\u043d\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u043c\u043d\u0435')])),
                ('pvt_actors', models.IntegerField(default=0, verbose_name='\u041b\u044e\u0431\u0438\u043c\u044b\u0435 \u0430\u043a\u0442\u0435\u0440\u044b \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', choices=[(0, '\u0412\u0438\u0434\u043d\u043e \u0432\u0441\u0435\u043c'), (1, '\u0412\u0438\u0434\u043d\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u0434\u0440\u0443\u0437\u044c\u044f\u043c'), (2, '\u0412\u0438\u0434\u043d\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u043c\u043d\u0435')])),
                ('pvt_directors', models.IntegerField(default=0, verbose_name='\u041b\u044e\u0431\u0438\u043c\u044b\u0435 \u0440\u0435\u0436\u0438\u0441\u0435\u0440\u044b \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f', choices=[(0, '\u0412\u0438\u0434\u043d\u043e \u0432\u0441\u0435\u043c'), (1, '\u0412\u0438\u0434\u043d\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u0434\u0440\u0443\u0437\u044c\u044f\u043c'), (2, '\u0412\u0438\u0434\u043d\u043e \u0442\u043e\u043b\u044c\u043a\u043e \u043c\u043d\u0435')])),
                ('confirm_email', models.BooleanField(default=False, verbose_name='\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435 email \u043d\u0430 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0443 \u0438 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u044f')),
                ('user', models.OneToOneField(related_name='profile', verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users_profile',
                'verbose_name': '\u041f\u0440\u043e\u0444\u0438\u043b\u044c \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u041f\u0440\u043e\u0444\u0438\u043b\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersRels',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rel_type', models.CharField(max_length=255, verbose_name='\u0422\u0438\u043f \u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u0439', choices=[(b'f', b'\xd0\x94\xd1\x80\xd1\x83\xd0\xb7\xd1\x8c\xd1\x8f'), (b's', b'\xd0\x97\xd0\xb0\xd1\x8f\xd0\xb2\xd0\xba\xd0\xb0 \xd0\xbe\xd1\x82\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb0, \xd0\xbd\xd0\xbe \xd0\xbd\xd0\xb5 \xd0\xbf\xd1\x80\xd0\xb8\xd0\xbd\xd1\x8f\xd1\x82\xd0\xb0'), (b'r', b'\xd0\x97\xd0\xb0\xd1\x8f\xd0\xb2\xd0\xba\xd0\xb0 \xd0\xbf\xd0\xbe\xd0\xbb\xd1\x83\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb0, \xd0\xbd\xd0\xbe \xd0\xbd\xd0\xb5 \xd0\xbf\xd1\x80\xd0\xb8\xd0\xbd\xd1\x8f\xd1\x82\xd0\xb0')])),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f/\u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f')),
                ('user', models.ForeignKey(related_name='rels', verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438', to=settings.AUTH_USER_MODEL)),
                ('user_rel', models.ForeignKey(related_name='user_rel', verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users_rels',
                'verbose_name': '\u041e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
                'verbose_name_plural': '\u041e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u044f \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='usersrels',
            unique_together=set([('user', 'user_rel')]),
        ),
    ]
