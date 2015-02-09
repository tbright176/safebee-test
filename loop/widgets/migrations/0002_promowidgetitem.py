# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__first__'),
        ('widgets', '0001_initial'),
        ('asset_manager', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoWidgetItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('widget', models.ForeignKey(to='widgets.PromoWidget', to_field='id')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', to_field='id')),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(help_text=b"Optional. Use to override the content_object's title.", max_length=40, null=True, blank=True)),
                ('link', models.URLField(help_text=b"Optional. Use to override the content_object's URL. You may link to arbitrary URL in this field.", null=True, blank=True)),
                ('description', models.CharField(help_text=b"Optional. Use to override the content_object's description.", max_length=75, null=True, blank=True)),
                ('image', models.ForeignKey(to_field='id', blank=True, to='asset_manager.Image', help_text=b"Optional. Use to override the content_object's image.", null=True)),
                ('order', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': [b'order'],
            },
            bases=(models.Model,),
        ),
    ]
