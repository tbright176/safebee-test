# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0007_auto_20140829_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scorerange',
            name='image',
        ),
        migrations.AlterField(
            model_name='quiz',
            name='related',
            field=models.ManyToManyField(to=b'core.StreamItem', null=True, blank=True),
        ),
    ]
