# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('recalls', '0016_auto_20141212_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecallAlert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('published', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('topic', models.ForeignKey(to='recalls.RecallSNSTopic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
