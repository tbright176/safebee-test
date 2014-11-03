# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('recalls', '0003_auto_20141031_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecallStreamItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('organization', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(0, b'CPSC'), (1, b'FDA'), (2, b'NHTSA'), (3, b'USDA')])),
                ('recall_subject', models.TextField(blank=True)),
                ('recall_number', models.CharField(db_index=True, max_length=50, blank=True)),
                ('recall_url', models.URLField(blank=True)),
                ('recall_date', models.DateField(null=True, blank=True)),
                ('name', models.TextField(blank=True)),
                ('initiator', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('corrective_summary', models.TextField(blank=True)),
                ('consequence_summary', models.TextField(blank=True)),
                ('defect_summary', models.TextField(blank=True)),
                ('contact_summary', models.TextField(blank=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(max_length=255, null=True, upload_to=b'assets/recalls/images', blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='carrecall',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 3, 17, 22, 7, 994467), auto_now_add=True, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carrecall',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 3, 17, 22, 12, 889264), auto_now=True, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foodrecall',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 3, 17, 22, 27, 337465), auto_now_add=True, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foodrecall',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 3, 17, 22, 32, 448364), auto_now=True, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productrecall',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 3, 17, 22, 39, 865026), auto_now_add=True, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productrecall',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 3, 17, 22, 48, 695898), auto_now=True, db_index=True),
            preserve_default=False,
        ),
    ]
