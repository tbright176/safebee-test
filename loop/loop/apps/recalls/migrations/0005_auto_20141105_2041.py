# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0004_auto_20141103_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrecall',
            name='image',
            field=models.ImageField(max_length=255, null=True, upload_to=b'assets/recalls/images', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='foodrecall',
            name='image',
            field=models.ImageField(max_length=255, null=True, upload_to=b'assets/recalls/images', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='productrecall',
            name='image',
            field=models.ImageField(max_length=255, null=True, upload_to=b'assets/recalls/images', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recallstreamitem',
            name='image',
            field=models.ImageField(max_length=255, null=True, upload_to=b'assets/recalls/images', blank=True),
            preserve_default=True,
        ),
    ]
