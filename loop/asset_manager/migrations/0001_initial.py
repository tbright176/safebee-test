# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import loop.asset_manager.models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.TextField()),
                ('display_caption', models.BooleanField(default=True)),
                ('notes', models.TextField(help_text=b'Optional. For internal use only.', null=True, blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name=b'last modified', auto_now_add=True)),
                ('asset_author', models.CharField(max_length=255, null=True, blank=True)),
                ('asset_source', models.CharField(max_length=255, null=True, blank=True)),
                ('asset_organization', models.CharField(max_length=255, null=True, blank=True)),
                ('asset_organization_source', models.CharField(max_length=255, null=True, blank=True)),
                ('asset', easy_thumbnails.fields.ThumbnailerImageField(help_text=b'Required. Upload a larger version of the asset than is needed, as it will be scaled and cropped automatically to fit the template as required.', max_length=255, upload_to=loop.asset_manager.models.image_asset_storage_path)),
                ('social_asset', easy_thumbnails.fields.ThumbnailerImageField(help_text=b'Optional. If defined, this will be used as the representation of the image on social media.', max_length=255, null=True, upload_to=loop.asset_manager.models.image_asset_storage_subpath, blank=True)),
                ('promo_asset', easy_thumbnails.fields.ThumbnailerImageField(help_text=b'Optional. If defined, this will be used as the representation of the image in promo spots across the site.', max_length=255, null=True, upload_to=loop.asset_manager.models.image_asset_storage_subpath, blank=True)),
                ('created_by', models.ForeignKey(to_field='id', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': [b'-creation_date'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('link', models.URLField(null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': [b'name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='image',
            name='asset_license',
            field=models.ForeignKey(to_field='id', blank=True, to='asset_manager.License', null=True),
            preserve_default=True,
        ),
    ]
