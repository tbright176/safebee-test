# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0003_featureditem_primary_feature'),
    ]

    operations = [
        migrations.AddField(
            model_name='featureditem',
            name='title',
            field=models.CharField(help_text=b"Optional. Use to override the content item's title.", max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='featureditem',
            name='url',
            field=models.URLField(help_text=b"Optional. Use to override the content item's URL. You may link to an arbitrary URL in this field.", null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='featureditem',
            name='image',
            field=models.ForeignKey(related_name=b'features_featureditem_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b"Optional. Use to override the content item's image.", null=True),
        ),
    ]
