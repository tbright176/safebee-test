# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20140717_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='primary_image_caption_override',
            field=models.TextField(help_text=b'If set, this field will override the caption and credit provided by the primary image asset.', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
