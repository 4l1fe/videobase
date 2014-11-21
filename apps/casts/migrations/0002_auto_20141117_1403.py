# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('casts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='castschatsusers',
            name='status',
            field=models.CharField(default=b'offline', max_length=255, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', db_index=True, choices=[(b'online', '\u041e\u043d\u043b\u0430\u0439\u043d'), (b'offline', '\u041e\u0444\u043b\u0430\u0439\u043d'), (b'blocked', '\u0417\u0430\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u0430\u043d')]),
            preserve_default=True,
        ),
    ]
