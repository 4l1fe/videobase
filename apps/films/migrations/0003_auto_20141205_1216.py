# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_auto_20141110_1057'),
    ]

    operations = [
        migrations.RunSQL("DROP INDEX IF EXISTS films_search_index;"),
        migrations.RunSQL("CREATE INDEX films_search_index ON films USING GIN(search_index);"),
    ]
