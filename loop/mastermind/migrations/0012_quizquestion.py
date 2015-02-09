# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0011_quiz_exclude_from_most_popular'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField()),
                ('question', models.ForeignKey(to='mastermind.Question')),
                ('quiz', models.ForeignKey(to='mastermind.Quiz')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
