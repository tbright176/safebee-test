# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JSONAPIResponseRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('social_service', models.CharField(max_length=2, choices=[(b'D', b'Disqus'), (b'T', b'Twitter')])),
                ('json', jsonfield.fields.JSONField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='socialstatusrecord',
            name='social_service',
            field=models.CharField(max_length=2, choices=[(b'D', b'Disqus'), (b'T', b'Twitter')]),
            preserve_default=True,
        ),
    ]
