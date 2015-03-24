# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_photoblog_intro'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamitem',
            name='secondary_author',
            field=models.ForeignKey(related_name='secondary_author', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='streamitem',
            name='author',
            field=models.ForeignKey(related_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
