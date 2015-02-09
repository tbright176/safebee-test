# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20141103_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisqusThread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('thread_type', models.CharField(max_length=2, choices=[(b'H', b'Hot'), (b'P', b'Popular')])),
                ('thread_link', models.URLField()),
                ('thread_posts', models.PositiveIntegerField(default=0)),
                ('thread_likes', models.PositiveIntegerField(default=0)),
                ('thread_title', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
