# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20140919_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuzzStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False)),
                ('stream_item', models.ForeignKey(to='core.StreamItem')),
            ],
            options={
                'ordering': ['active', 'stream_item'],
            },
            bases=(models.Model,),
        ),
    ]
