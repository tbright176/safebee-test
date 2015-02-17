# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0004_auto_20140929_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='intro_copy',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
