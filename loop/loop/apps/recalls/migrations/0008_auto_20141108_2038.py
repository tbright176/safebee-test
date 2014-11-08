# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0007_auto_20141105_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarMake',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='make')),
                ('logo', models.ImageField(max_length=255, null=True, upload_to=b'assets/recalls/makes', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='carrecallrecord',
            name='make',
        ),
        migrations.AddField(
            model_name='carrecallrecord',
            name='vehicle_make',
            field=models.ForeignKey(blank=True, to='recalls.CarMake', null=True),
            preserve_default=True,
        ),
    ]
