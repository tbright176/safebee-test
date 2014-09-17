# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0006_auto_20140828_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='results_image',
            field=models.ForeignKey(blank=True, to='asset_manager.Image', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='background_image',
            field=models.ForeignKey(blank=True, to='asset_manager.Image', null=True),
        ),
    ]
