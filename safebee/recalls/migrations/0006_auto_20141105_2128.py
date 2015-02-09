# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0005_auto_20141105_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrecall',
            name='slug',
            field=models.SlugField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foodrecall',
            name='slug',
            field=models.SlugField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productrecall',
            name='slug',
            field=models.SlugField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
