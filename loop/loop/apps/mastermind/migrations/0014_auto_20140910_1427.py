# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0013_remove_question_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.AlterField(
            model_name='quizquestion',
            name='question',
            field=models.OneToOneField(to='mastermind.Question'),
        ),
    ]
