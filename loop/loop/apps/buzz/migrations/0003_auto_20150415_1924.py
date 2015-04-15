# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buzz', '0002_auto_20140919_1652'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buzzstory',
            options={'ordering': ['-active', 'stream_item'], 'verbose_name_plural': 'Buzz Stories'},
        ),
    ]
