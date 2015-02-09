# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0002_featureditem_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='featureditem',
            name='primary_feature',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
