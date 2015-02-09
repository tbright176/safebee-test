# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0012_quizquestion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='order',
        ),
    ]
