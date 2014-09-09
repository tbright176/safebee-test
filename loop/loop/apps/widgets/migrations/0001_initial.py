# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset_manager', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoWidget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(unique=True, max_length=100)),
                ('show_header', models.BooleanField(default=False)),
                ('header_image', models.ForeignKey(to_field='id', blank=True, to='asset_manager.Image', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
