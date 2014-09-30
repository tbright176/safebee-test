# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset_manager', '0004_auto_20140910_1544'),
        ('features', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='featureditem',
            name='image',
            field=models.ForeignKey(related_name=b'features_featureditem_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', null=True),
            preserve_default=True,
        ),
    ]
