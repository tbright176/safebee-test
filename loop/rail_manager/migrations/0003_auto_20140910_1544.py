# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rail_manager', '0002_module_widget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='railitem',
            name='rail',
            field=models.ForeignKey(related_name=b'items', to='rail_manager.Rail'),
        ),
    ]
