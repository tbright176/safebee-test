# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset_manager', '0003_auto_20140710_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='asset_organization_source',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Organization URL', blank=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='asset_source',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Author URL', blank=True),
        ),
    ]
