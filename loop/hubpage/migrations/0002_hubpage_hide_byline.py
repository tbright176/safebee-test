# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hubpage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hubpage',
            name='hide_byline',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
