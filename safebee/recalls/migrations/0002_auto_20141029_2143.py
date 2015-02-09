# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrecall',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(max_length=255, null=True, upload_to=b'assets/recalls/images', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='foodrecall',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(max_length=255, null=True, upload_to=b'assets/recalls/images', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='productrecall',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(max_length=255, null=True, upload_to=b'assets/recalls/images', blank=True),
            preserve_default=True,
        ),
    ]
