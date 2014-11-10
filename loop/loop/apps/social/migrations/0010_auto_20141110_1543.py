# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('social', '0009_mostpopularrecall_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mostpopularrecall',
            name='image',
        ),
        migrations.AddField(
            model_name='mostpopularrecall',
            name='content_type',
            field=models.ForeignKey(default=1, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mostpopularrecall',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
