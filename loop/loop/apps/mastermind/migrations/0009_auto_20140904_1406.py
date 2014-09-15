# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0008_auto_20140902_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='explanation',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='results_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', null=True),
        ),
    ]
