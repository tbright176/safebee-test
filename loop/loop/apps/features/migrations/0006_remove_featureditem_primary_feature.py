# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0005_feature_intro_copy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featureditem',
            name='primary_feature',
        ),
    ]
