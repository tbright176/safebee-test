# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flatpage',
            name='modification_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 7, 3, 13, 43, 15, 222622), auto_now=True, auto_now_add=True, verbose_name='last modified'),
            preserve_default=False,
        ),
    ]
