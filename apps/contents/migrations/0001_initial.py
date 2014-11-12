# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from decimal import Decimal
import utils.fields.currency_field


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'about',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='T\u0435\u043a\u0441\u0442 \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u044f')),
                ('parent_id', models.IntegerField(null=True, verbose_name='\u0420\u043e\u0434\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u0438\u0439 \u043a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439', blank=True)),
                ('status', models.PositiveIntegerField(null=True, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0421\u043e\u0437\u0434\u0430\u043d', db_index=True)),
            ],
            options={
                'db_table': 'comments',
                'verbose_name': '\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439',
                'verbose_name_plural': '\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('name_orig', models.CharField(max_length=255, verbose_name='\u041e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u044c\u043d\u043e\u0435 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('number', models.IntegerField(null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0441\u0435\u0437\u043e\u043d\u0430', blank=True)),
                ('description', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('release_date', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0432\u044b\u0445\u043e\u0434\u0430')),
                ('viewer_cnt', models.IntegerField(verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u043e\u0441\u043c\u043e\u0442\u0440\u0435\u0432\u0448\u0438\u0445 \u0437\u0430 \u0432\u0441\u0435 \u0432\u0440\u0435\u043c\u044f')),
                ('viewer_lastweek_cnt', models.IntegerField(verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u043e\u0441\u043c\u043e\u0442\u0440\u0435\u0432\u0448\u0438\u0445 \u0437\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u044e\u044e \u043d\u0435\u0434\u0435\u043b\u044e')),
                ('viewer_lastmonth_cnt', models.IntegerField(verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u043e\u0441\u043c\u043e\u0442\u0440\u0435\u0432\u0448\u0438\u0445 \u0437\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0438\u0439 \u043c\u0435\u0441\u044f\u0446o')),
                ('film', models.ForeignKey(related_name='contents', verbose_name='\u0424\u0438\u043b\u044c\u043c', to='films.Films')),
                ('season', models.ForeignKey(verbose_name='\u0421\u0435\u0437\u043e\u043d\u044b', blank=True, to='films.Seasons', null=True)),
            ],
            options={
                'db_table': 'content',
                'verbose_name': '\u041a\u043e\u043d\u0442\u0435\u043d\u0442',
                'verbose_name_plural': '\u041a\u043e\u043d\u0442\u0435\u043d\u0442',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Legal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'legal',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(db_index=True, max_length=40, verbose_name='\u0422\u0438\u043f', choices=[(b'ivi', b'ivi'), (b'zoomby', b'zoomby'), (b'megogo', b'megogo'), (b'tvigle', b'tvigle'), (b'playfamily', b'playfamily'), (b'amediateka', b'amediateka'), (b'molodejj', b'molodejj'), (b'nowru', b'nowru'), (b'streamru', b'streamru'), (b'tvzavr', b'tvzavr'), (b'viaplay', b'viaplay'), (b'zabavaru', b'zabavaru'), (b'tvzorru', b'tvzorru'), (b'playgoogle', b'playgoogle'), (b'itunes', b'itunes'), (b'ayyo', b'ayyo'), (b'mosfilm', b'mosfilm'), (b'olltv', b'olltv'), (b'0', b'0')])),
                ('lang', models.CharField(max_length=40, verbose_name='\u042f\u0437\u044b\u043a')),
                ('quality', models.CharField(max_length=40, verbose_name='\u041a\u0430\u0447\u0435\u0441\u0442\u0432\u043e')),
                ('subtitles', models.CharField(max_length=40, verbose_name='\u0421\u0443\u0431\u0442\u0438\u0442\u0440\u044b')),
                ('price', utils.fields.currency_field.CurrencyField(default=Decimal('0.0'), verbose_name='\u0426\u0435\u043d\u0430', max_digits=30, decimal_places=2, db_index=True)),
                ('price_type', models.SmallIntegerField(db_index=True, verbose_name='\u0422\u0438\u043f \u0446\u0435\u043d\u044b', choices=[(0, b'\xd0\x91\xd0\xb5\xd1\x81\xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd0\xbd\xd0\xbe'), (1, b'\xd0\x9f\xd0\xbe \xd0\xbf\xd0\xbe\xd0\xb4\xd0\xbf\xd0\xb8\xd1\x81\xd0\xba\xd0\xb5'), (2, b'\xd0\x9f\xd0\xbb\xd0\xb0\xd1\x82\xd0\xbd\xd0\xbe')])),
                ('url_view', models.URLField(max_length=255, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u0434\u043b\u044f \u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u0430')),
                ('value', models.TextField(null=True, verbose_name='\u041a\u043e\u0434 \u0432\u0441\u0442\u0440\u0430\u0438\u0432\u0430\u043d\u0438\u044f', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u0421\u043e\u0437\u0434\u0430\u043d')),
                ('content', models.ForeignKey(related_name='location', verbose_name='\u041a\u043e\u043d\u0442\u0435\u043d\u0442', to='contents.Contents')),
            ],
            options={
                'db_table': 'locations',
                'verbose_name': '\u041c\u0435\u0441\u0442\u043e\u0440\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u043a\u043e\u043d\u0442\u0435\u043d\u0442\u0430',
                'verbose_name_plural': '\u041c\u0435\u0441\u0442\u043e\u0440\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u043a\u043e\u043d\u0442\u0435\u043d\u0442\u0430',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comments',
            name='content',
            field=models.ForeignKey(verbose_name='\u041a\u043e\u043d\u0442\u0435\u043d\u0442', to='contents.Contents'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(related_name='comments', verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
