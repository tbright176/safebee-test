# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0017_recallalert'),
    ]

    operations = [
        migrations.CreateModel(
            name='ULPublicNotice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notice_date', models.DateTimeField(null=True, blank=True)),
                ('notice_title', models.CharField(max_length=255)),
                ('notice_link', models.URLField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['-notice_date'],
            },
            bases=(models.Model,),
        ),
    ]
