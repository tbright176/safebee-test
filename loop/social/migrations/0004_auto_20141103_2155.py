# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_disqusthread'),
    ]

    operations = [
        migrations.DeleteModel(
            name='JSONAPIResponseRecord',
        ),
        migrations.AlterModelOptions(
            name='disqusthread',
            options={'ordering': ['-creation_date']},
        ),
        migrations.AddField(
            model_name='disqusthread',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 3, 21, 55, 59, 105302, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
