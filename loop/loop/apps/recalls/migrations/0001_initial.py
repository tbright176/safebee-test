# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarRecall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization', models.PositiveSmallIntegerField(choices=[(0, b'CPSC'), (1, b'FDA'), (2, b'NHTSA'), (3, b'USDA')])),
                ('recall_subject', models.CharField(max_length=50)),
                ('recall_number', models.CharField(max_length=50, db_index=True)),
                ('recall_url', models.URLField()),
                ('recall_date', models.DateField()),
                ('initiator', models.CharField(max_length=50)),
                ('notes', models.TextField()),
                ('corrective_summary', models.TextField()),
                ('consequence_summary', models.TextField()),
                ('defect_summary', models.TextField()),
                ('code', models.CharField(max_length=1, verbose_name='code')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CarRecallRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recalled_component_id', models.CharField(max_length=50, verbose_name='recall component identifier')),
                ('component_description', models.CharField(max_length=50, verbose_name='component description')),
                ('manufacturer', models.CharField(max_length=100, verbose_name='manufacturer')),
                ('manufacturing_begin_date', models.DateField(verbose_name='manufacturing begin date', blank=True)),
                ('manufacturing_end_date', models.DateField(verbose_name='manufacturing end date', blank=True)),
                ('make', models.CharField(max_length=50, verbose_name='make', blank=True)),
                ('model', models.CharField(max_length=50, verbose_name='model', blank=True)),
                ('year', models.PositiveSmallIntegerField(max_length=4, verbose_name='year', blank=True)),
                ('recall', models.ForeignKey(to='recalls.CarRecall')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FoodRecall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization', models.PositiveSmallIntegerField(choices=[(0, b'CPSC'), (1, b'FDA'), (2, b'NHTSA'), (3, b'USDA')])),
                ('recall_subject', models.CharField(max_length=50)),
                ('recall_number', models.CharField(max_length=50, db_index=True)),
                ('recall_url', models.URLField()),
                ('recall_date', models.DateField()),
                ('initiator', models.CharField(max_length=50)),
                ('notes', models.TextField()),
                ('corrective_summary', models.TextField()),
                ('consequence_summary', models.TextField()),
                ('defect_summary', models.TextField()),
                ('food_type', models.CharField(max_length=1, verbose_name='Food Recall Type', blank=True)),
                ('description', models.TextField(blank=True)),
                ('summary', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductRecall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization', models.PositiveSmallIntegerField(choices=[(0, b'CPSC'), (1, b'FDA'), (2, b'NHTSA'), (3, b'USDA')])),
                ('recall_subject', models.CharField(max_length=50)),
                ('recall_number', models.CharField(max_length=50, db_index=True)),
                ('recall_url', models.URLField()),
                ('recall_date', models.DateField()),
                ('initiator', models.CharField(max_length=50)),
                ('notes', models.TextField()),
                ('corrective_summary', models.TextField()),
                ('consequence_summary', models.TextField()),
                ('defect_summary', models.TextField()),
                ('upc', models.CharField(max_length=64, verbose_name='UPC', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
