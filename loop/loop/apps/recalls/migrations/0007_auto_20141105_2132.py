# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0006_auto_20141105_2128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carrecall',
            options={'ordering': ['-recall_date']},
        ),
        migrations.AlterModelOptions(
            name='foodrecall',
            options={'ordering': ['-recall_date']},
        ),
        migrations.AlterModelOptions(
            name='productrecall',
            options={'ordering': ['-recall_date']},
        ),
        migrations.AlterModelOptions(
            name='recallstreamitem',
            options={},
        ),
    ]
