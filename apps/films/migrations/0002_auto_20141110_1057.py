# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS unaccent"),
        migrations.RunSQL("CREATE text search configuration public.film_names (parser='default')"),
        migrations.RunSQL("ALTER text search configuration film_names alter mapping for asciiword, asciihword, hword_asciipart, hword_numpart, word, hword, numword, hword_part with unaccent, simple"),
    ]
