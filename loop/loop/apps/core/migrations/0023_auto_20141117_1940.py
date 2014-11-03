# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20140919_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='loopuser',
            name='include_on_about_page',
            field=models.BooleanField(default=False, help_text=b'Enable to include this user on the About Us page'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loopuser',
            name='inclusion_ordering',
            field=models.PositiveSmallIntegerField(default=0, help_text=b'For users included on the about page, this field controls the ordering. If two or more users share the same order, then they will be sorted alphabetically.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loopuser',
            name='title',
            field=models.TextField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
    ]
