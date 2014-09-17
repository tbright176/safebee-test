# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0003_auto_20140826_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='related',
            field=models.ManyToManyField(to=b'core.StreamItem'),
            preserve_default=True,
        ),
    ]
