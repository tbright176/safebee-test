# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_nonauth_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='meta_description',
            field=models.CharField(help_text=b'Max 150 characters.', max_length=150, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='meta_description',
            field=models.CharField(help_text=b'Max 150 characters.', max_length=150, null=True, blank=True),
            preserve_default=True,
        ),
    ]
