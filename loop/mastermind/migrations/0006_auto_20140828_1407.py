# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0005_auto_20140826_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='explanation',
            field=models.CharField(default='', max_length=350),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scorerange',
            name='image',
            field=models.ForeignKey(blank=True, to='asset_manager.Image', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='background_image',
            field=models.ForeignKey(to='asset_manager.Image'),
        ),
    ]
