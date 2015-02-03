# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hubpage', '0004_hubpagefeatureditem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hubpagefeatureditem',
            name='hide_title_and_description',
        ),
    ]
