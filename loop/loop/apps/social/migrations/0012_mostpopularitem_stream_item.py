# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_tag_internal_use_only'),
        ('social', '0011_popularlast7daysitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='mostpopularitem',
            name='stream_item',
            field=models.ForeignKey(verbose_name=b'Content Item', blank=True, to='core.StreamItem', null=True),
            preserve_default=True,
        ),
    ]
