# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rail_manager', '0001_initial'),
        ('widgets', '0003_auto_20140604_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='widget',
            field=models.ForeignKey(to_field='id', blank=True, to='widgets.PromoWidget', null=True),
            preserve_default=True,
        ),
    ]
