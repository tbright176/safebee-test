# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relateditem',
            options={'ordering': [b'order']},
        ),
        migrations.AlterField(
            model_name='relateditem',
            name='stream_item',
            field=models.ForeignKey(verbose_name=b'Content Item', blank=True, to='core.StreamItem', null=True),
        ),
    ]
