# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0015_carmodel_years'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrecall',
            name='api_json',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foodrecall',
            name='api_json',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productrecall',
            name='api_json',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
