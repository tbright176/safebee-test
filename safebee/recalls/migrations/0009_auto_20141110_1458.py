# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0008_auto_20141108_2038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carmake',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='carmake',
            name='show_in_results',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
