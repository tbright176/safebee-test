# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20150324_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='internal_use_only',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
