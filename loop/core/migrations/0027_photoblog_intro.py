# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20141215_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='photoblog',
            name='intro',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
    ]
