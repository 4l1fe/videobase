# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usershash',
            name='activated',
            field=models.BooleanField(default=False, verbose_name='\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usersrels',
            name='rel_type',
            field=models.CharField(max_length=255, verbose_name='\u0422\u0438\u043f \u043e\u0442\u043d\u043e\u0448\u0435\u043d\u0438\u0439', choices=[(b'f', b'\xd0\x94\xd1\x80\xd1\x83\xd0\xb7\xd1\x8c\xd1\x8f'), (b'', b'\xd0\x9d\xd0\xb5\xd1\x82\xd1\x83 \xd0\xbe\xd1\x82\xd0\xbd\xd0\xbe\xd1\x88\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb9'), (b's', b'\xd0\x97\xd0\xb0\xd1\x8f\xd0\xb2\xd0\xba\xd0\xb0 \xd0\xbe\xd1\x82\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb0, \xd0\xbd\xd0\xbe \xd0\xbd\xd0\xb5 \xd0\xbf\xd1\x80\xd0\xb8\xd0\xbd\xd1\x8f\xd1\x82\xd0\xb0'), (b'r', b'\xd0\x97\xd0\xb0\xd1\x8f\xd0\xb2\xd0\xba\xd0\xb0 \xd0\xbf\xd0\xbe\xd0\xbb\xd1\x83\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb0, \xd0\xbd\xd0\xbe \xd0\xbd\xd0\xb5 \xd0\xbf\xd1\x80\xd0\xb8\xd0\xbd\xd1\x8f\xd1\x82\xd0\xb0')]),
            preserve_default=True,
        ),
    ]
