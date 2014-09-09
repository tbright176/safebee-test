# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '__latest__'),
        ('asset_manager', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Optional. Leave blank to use the category title, or if no category is not set, display no title.', max_length=100, null=True, blank=True)),
                ('active', models.BooleanField(default=False, help_text=b'Uncheck to remove this module from all pages it displays on.')),
                ('category', models.ForeignKey(to_field='id', blank=True, to='core.Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentModuleItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('featured', models.BooleanField(default=False)),
                ('content_title', models.CharField(help_text=b"Optional. Use to override the content object's title.", max_length=255, null=True, blank=True)),
                ('content_description', models.CharField(help_text=b"Optional. Use to override the content object's description.", max_length=255, null=True, blank=True)),
                ('content_url', models.URLField(help_text=b"Optional. Use to override the content object's URL.", null=True, blank=True)),
                ('order', models.PositiveIntegerField()),
                ('content_image', models.ForeignKey(to_field='id', blank=True, to='asset_manager.Image', help_text=b"Optional. Use to override the content object's promo image.", null=True)),
                ('content_object', models.ForeignKey(to_field='id', blank=True, to='core.StreamItem', help_text=b'Optional. If you do not select a content object, you must fill out all of the fields below.', null=True)),
                ('module', models.ForeignKey(to='hubpage.ContentModule', to_field='id')),
            ],
            options={
                'ordering': [b'order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HubPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('set_as_homepage', models.BooleanField(default=False)),
                ('featured_content_title', models.CharField(help_text=b"Optional. Use to override the featured story's title.", max_length=255, null=True, blank=True)),
                ('featured_content_description', models.CharField(help_text=b"Optional. Use to override the featured story's description.", max_length=255, null=True, blank=True)),
                ('featured_content_url', models.URLField(help_text=b"Optional. Use to override the featured story's URL.", null=True, blank=True)),
                ('featured_content', models.ForeignKey(to_field='id', blank=True, to='core.StreamItem', help_text=b'Optional. If you do not select a featured story, you must fill out all of the fields below.', null=True)),
                ('featured_content_image', models.ForeignKey(to_field='id', blank=True, to='asset_manager.Image', help_text=b"Optional. Use to override the featured story's promo image.", null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contentmodule',
            name='hubpage',
            field=models.ForeignKey(to_field='id', blank=True, to='hubpage.HubPage', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='HubPageCategoryContentModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_featured_story_only', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField()),
                ('hubpage', models.ForeignKey(to='hubpage.HubPage', to_field='id')),
                ('module', models.ForeignKey(to='hubpage.ContentModule', to_field='id')),
            ],
            options={
                'ordering': [b'order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HubPageContentModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField()),
                ('hubpage', models.ForeignKey(to='hubpage.HubPage', to_field='id')),
                ('module', models.ForeignKey(to='hubpage.ContentModule', to_field='id')),
            ],
            options={
                'ordering': [b'order'],
            },
            bases=(models.Model,),
        ),
    ]
