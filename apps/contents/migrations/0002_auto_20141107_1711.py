# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='content_type',
            field=models.CharField(db_index=True, max_length=40, null=True, verbose_name='\u0422\u0438\u043f \u043e\u0431\u044a\u0435\u043a\u0442\u0430', choices=[(b'FILM', '\u0424\u0438\u043b\u044c\u043c'), (b'SEASON', '\u0421\u0435\u0437\u043e\u043d'), (b'EPISODE', '\u0421\u0435\u0440\u0438\u044f')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locations',
            name='episode',
            field=models.IntegerField(null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0441\u0435\u0440\u0438\u0438', blank=True),
            preserve_default=True,
        ),
    ]
