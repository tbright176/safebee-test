# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0017_quiz_intro_copy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='intro_copy',
            field=models.CharField(help_text=b'The text to be used on the intro slide of the quiz. If left empty, the description will be used instead.', max_length=160, null=True, blank=True),
            preserve_default=True,
        ),
    ]
