# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0009_auto_20140904_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='secondary_author',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='related',
        ),
    ]
