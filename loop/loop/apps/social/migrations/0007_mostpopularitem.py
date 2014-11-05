# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_auto_20141104_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='MostPopularItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(max_length=255)),
                ('link', models.URLField()),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
    ]
