# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_nonauth_initial'),
        ('widgets', '0002_promowidgetitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='promowidgetitem',
            name='content_item',
            field=models.ForeignKey(to='core.StreamItem', default=0, to_field='id'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='promowidgetitem',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='promowidgetitem',
            name='content_type',
        ),
    ]
