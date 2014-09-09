# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(default=b'D', max_length=1, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled'), (b'T', b'Trash')]),
        ),
        migrations.AlterField(
            model_name='slideshow',
            name='status',
            field=models.CharField(default=b'D', max_length=1, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled'), (b'T', b'Trash')]),
        ),
        migrations.AlterField(
            model_name='streamitem',
            name='status',
            field=models.CharField(default=b'D', max_length=1, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled'), (b'T', b'Trash')]),
        ),
    ]
