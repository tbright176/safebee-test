# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20140703_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='loopuser',
            name='bio',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loopuser',
            name='google_plus_profile_url',
            field=models.URLField(help_text=b'Google+ Profile URL', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loopuser',
            name='twitter',
            field=models.CharField(help_text=b'Twitter username', max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
