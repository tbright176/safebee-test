# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0004_quiz_related'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='status',
            field=models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Draft'), (b'M', b'Moderate 0'), (b'M1', b'Moderate 1'), (b'M2', b'Moderate 2'), (b'F', b'Final Review'), (b'R', b'Ready for Pub'), (b'P', b'Published'), (b'S', b'Scheduled'), (b'T', b'Trash')]),
        ),
    ]
