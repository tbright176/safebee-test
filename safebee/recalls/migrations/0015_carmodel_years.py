# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0014_carmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodel',
            name='years',
            field=models.CommaSeparatedIntegerField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
