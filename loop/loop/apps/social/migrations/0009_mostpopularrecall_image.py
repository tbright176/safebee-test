# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0008_mostpopularrecall'),
    ]

    operations = [
        migrations.AddField(
            model_name='mostpopularrecall',
            name='image',
            field=models.ImageField(max_length=255, null=True, upload_to=b'assets/recalls/images', blank=True),
            preserve_default=True,
        ),
    ]
