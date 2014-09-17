# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_nonauth_initial'),
        ('mastermind', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='category',
            field=models.ForeignKey(default=1, to='core.Category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quiz',
            name='background_image',
            field=models.ForeignKey(to='asset_manager.Image'),
        ),
    ]
