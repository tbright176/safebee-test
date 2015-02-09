# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buzz', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buzzstory',
            options={'ordering': ['active', 'stream_item'], 'verbose_name_plural': 'Buzz Stories'},
        ),
        migrations.AlterField(
            model_name='buzzstory',
            name='stream_item',
            field=models.ForeignKey(to='core.StreamItem', unique=True),
        ),
    ]
