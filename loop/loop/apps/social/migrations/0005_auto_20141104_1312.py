# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_auto_20141103_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disqusthread',
            name='creation_date',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
