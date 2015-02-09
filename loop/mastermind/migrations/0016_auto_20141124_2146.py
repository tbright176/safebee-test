# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0015_auto_20140915_1523'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quizquestion',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='quiz',
            name='status',
            field=models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled')]),
            preserve_default=True,
        ),
    ]
