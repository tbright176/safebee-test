# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset_manager', '0002_image_alt_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='alt_text',
            field=models.CharField(max_length=255),
        ),
    ]
