# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__first__'),
        ('asset_manager', '__first__'),
        ('core', '0014_auto_20140903_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('order', models.PositiveIntegerField(null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('image', models.ForeignKey(blank=True, to='asset_manager.Image', null=True)),
                ('stream_item', models.ForeignKey(to='core.StreamItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
