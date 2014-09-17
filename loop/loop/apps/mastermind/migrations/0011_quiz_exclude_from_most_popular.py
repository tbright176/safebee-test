# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0010_auto_20140904_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='exclude_from_most_popular',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
