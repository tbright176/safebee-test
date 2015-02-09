# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hubpage', '0002_hubpage_hide_byline'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentmodule',
            name='hide_featured_story_byline',
            field=models.BooleanField(default=False, help_text=b"Check to hide the featured story's byline on the category landing page."),
            preserve_default=True,
        ),
    ]
