# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0002_auto_20141029_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrecall',
            name='contact_summary',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carrecall',
            name='name',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foodrecall',
            name='contact_summary',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foodrecall',
            name='name',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productrecall',
            name='contact_summary',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productrecall',
            name='name',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
    ]
