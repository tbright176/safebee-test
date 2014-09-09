# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20140903_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='exclude_from_most_popular',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photooftheday',
            name='exclude_from_most_popular',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='slideshow',
            name='exclude_from_most_popular',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='streamitem',
            name='exclude_from_most_popular',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
