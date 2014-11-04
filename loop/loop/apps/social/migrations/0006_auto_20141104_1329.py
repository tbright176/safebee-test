# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_auto_20141104_1312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='disqusthread',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='disqusthread',
            name='order',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
