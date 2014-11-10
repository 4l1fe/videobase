# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KinopoiskTries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('try_time', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u043f\u044b\u0442\u043a\u0438')),
                ('result', models.CharField(max_length=255, verbose_name='\u0423\u0434\u0430\u043b\u0441\u044f \u043b\u0438 \u043f\u0430\u0440\u0441\u0438\u043d\u0433', choices=[(b'success', '\u0423\u0441\u043f\u0435\u0445'), (b'fail', '\u041d\u0435\u0443\u0434\u0430\u0447\u0430')])),
                ('error_message', models.TextField(null=True, verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 \u043e\u0431 \u043e\u0448\u0438\u0431\u043a\u0435')),
                ('page_dump', models.TextField(null=True, verbose_name='\u0421\u043a\u0430\u0447\u0430\u043d\u043d\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430')),
                ('film', models.ForeignKey(verbose_name='\u0424\u0438\u043b\u044c\u043c', to='films.Films')),
            ],
            options={
                'db_table': 'robots_kinopoisk_tries',
                'verbose_name': '\u041f\u043e\u043f\u044b\u0442\u043a\u0430 \u043a\u0438\u043d\u043e\u043f\u043e\u0438\u0441\u043a\u0430',
                'verbose_name_plural': '\u041f\u043e\u043f\u044b\u0442\u043a\u0438 \u043a\u0438\u043d\u043e\u043f\u043e\u0438\u0441\u043a\u0430',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocationsCorrectorLogging',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('robot_name', models.CharField(max_length=255, verbose_name='\u0418\u043c\u044f \u0440\u043e\u0431\u043e\u0442\u0430')),
                ('films', models.CharField(max_length=255, null=True, verbose_name='\u0424\u0438\u043b\u044c\u043c ')),
                ('log_time', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u043b\u043e\u0433\u0430')),
            ],
            options={
                'db_table': 'locations_corrector_logging',
                'verbose_name': '\u041b\u043e\u0433 \u043a\u043e\u0440\u0440\u0435\u043a\u0442\u043e\u0440\u0430',
                'verbose_name_plural': '\u041b\u043e\u0433\u0438 \u043a\u043e\u0440\u0440\u0435\u043a\u0442\u043e\u0440\u0430',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Robots',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False, verbose_name='\u0418\u043c\u044f', primary_key=True)),
                ('description', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0440\u043e\u0431\u043e\u0442\u0430')),
                ('last_start', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0433\u043e \u0441\u0442\u0430\u0440\u0442\u0430')),
                ('delay', models.IntegerField(verbose_name='\u0412\u0440\u0435\u043c\u044f \u043c\u0435\u0436\u0434\u0443 \u0441\u0442\u0430\u0440\u0442\u0430\u043c\u0438 \u0432 \u043c\u0438\u043d\u0443\u0442\u0430\u0445')),
                ('state', models.TextField(verbose_name='\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u043c\u0435\u0436\u0434\u0443 \u0437\u0430\u043f\u0443\u0441\u043a\u0430\u043c\u0438')),
            ],
            options={
                'db_table': 'robots',
                'verbose_name': '\u0420\u043e\u0431\u043e\u0442',
                'verbose_name_plural': '\u0420\u043e\u0431\u043e\u0442\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RobotsInfoLogging',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('robot_name', models.CharField(max_length=255, verbose_name='\u0418\u043c\u044f \u0440\u043e\u0431\u043e\u0442\u0430')),
                ('locations', models.CharField(max_length=255, verbose_name='\u041b\u043e\u043a\u0430\u0446\u0438\u0438')),
                ('films', models.CharField(max_length=255, null=True, verbose_name='\u0424\u0438\u043b\u044c\u043c\u044b ')),
                ('is_new_location', models.BooleanField(default=False, verbose_name='\u041d\u043e\u0432\u0430\u044f \u043b\u043e\u043a\u0430\u0446\u0438\u044f')),
                ('log_time', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u043b\u043e\u0433\u0430')),
            ],
            options={
                'db_table': 'robots_logging_info',
                'verbose_name': 'meta \u041b\u043e\u0433 \u0440\u043e\u0431\u043e\u0442\u0430',
                'verbose_name_plural': 'meta \u041b\u043e\u0433 \u0440\u043e\u0431\u043e\u0442\u043e\u0432',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RobotsLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043b\u0435\u0434\u0443\u044e\u0449\u0435\u0433\u043e \u0441\u0442\u0430\u0440\u0442\u0430')),
                ('value', models.CharField(max_length=255, verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435')),
                ('itype', models.IntegerField(verbose_name='\u0422\u0438\u043f')),
                ('try_time', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u043f\u044b\u0442\u043a\u0438')),
                ('robot_name', models.ForeignKey(verbose_name='\u0418\u043c\u044f \u0440\u043e\u0431\u043e\u0442\u0430', to='robots.Robots')),
            ],
            options={
                'db_table': 'robots_log',
                'verbose_name': '\u041b\u043e\u0433\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0440\u043e\u0431\u043e\u0442\u0430',
                'verbose_name_plural': '\u041b\u043e\u0433\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u0440\u043e\u0431\u043e\u0442\u043e\u0432',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RobotsMailList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=255, verbose_name='Email')),
            ],
            options={
                'db_table': 'robots_mail_list',
                'verbose_name': '\u0421\u043f\u0438\u0441\u043e\u043a \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438 \u0434\u043b\u044f \u0440\u043e\u0431\u043e\u0442\u0430',
                'verbose_name_plural': '\u0421\u043f\u0438\u0441\u043e\u043a \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438 \u0434\u043b\u044f \u0440\u043e\u0431\u043e\u0442\u043e\u0432',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RobotsTries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(max_length=255, verbose_name='\u0414\u043e\u043c\u0435\u043d')),
                ('url', models.URLField(max_length=255, null=True, verbose_name='URL to film information', blank=True)),
                ('outcome', models.CharField(max_length=255, verbose_name='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442', choices=[(b'sitefail', '\u0421\u0430\u0439\u0442 \u043d\u0435\u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d'), (b'pagefail', '\u041d\u0435\u0442 \u0442\u0430\u043a\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b'), (b'parsefail', '\u041e\u0448\u0438\u0431\u043a\u0430 \u043f\u0440\u0438 \u043f\u0430\u0440\u0441\u0438\u043d\u0433\u0435'), (b'success', '\u0414\u0430\u043d\u043d\u044b\u0435 \u0443\u0441\u043f\u0435\u0448\u043d\u043e \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u044b')])),
                ('film', models.ForeignKey(related_name='robots_tries', verbose_name='\u0424\u0438\u043b\u044c\u043c', to='films.Films')),
            ],
            options={
                'db_table': 'robots_tries',
                'verbose_name': '\u041f\u043e\u043f\u044b\u0442\u043a\u0430',
                'verbose_name_plural': '\u041f\u043e\u043f\u044b\u0442\u043a\u0438',
            },
            bases=(models.Model,),
        ),
    ]
