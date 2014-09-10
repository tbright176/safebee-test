# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20140905_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='primary_image',
            field=models.ForeignKey(related_name=b'core_article_primary_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='promo_image',
            field=models.ForeignKey(related_name=b'core_article_promo_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the promo image will be automatically created from the primary image.', null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='secondary_author',
            field=models.ForeignKey(related_name=b'+', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='social_image',
            field=models.ForeignKey(related_name=b'core_article_social_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the social image will be automatically created from the primary image.', null=True),
        ),
        migrations.AlterField(
            model_name='loopuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='loopuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='photooftheday',
            name='primary_image',
            field=models.ForeignKey(related_name=b'core_photooftheday_primary_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', null=True),
        ),
        migrations.AlterField(
            model_name='photooftheday',
            name='promo_image',
            field=models.ForeignKey(related_name=b'core_photooftheday_promo_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the promo image will be automatically created from the primary image.', null=True),
        ),
        migrations.AlterField(
            model_name='photooftheday',
            name='secondary_author',
            field=models.ForeignKey(related_name=b'+', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='photooftheday',
            name='social_image',
            field=models.ForeignKey(related_name=b'core_photooftheday_social_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the social image will be automatically created from the primary image.', null=True),
        ),
        migrations.AlterField(
            model_name='slide',
            name='image',
            field=models.ForeignKey(related_name=b'core_slide_primary_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', null=True),
        ),
        migrations.AlterField(
            model_name='slideshow',
            name='primary_image',
            field=models.ForeignKey(related_name=b'core_slideshow_primary_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', null=True),
        ),
        migrations.AlterField(
            model_name='slideshow',
            name='promo_image',
            field=models.ForeignKey(related_name=b'core_slideshow_promo_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the promo image will be automatically created from the primary image.', null=True),
        ),
        migrations.AlterField(
            model_name='slideshow',
            name='secondary_author',
            field=models.ForeignKey(related_name=b'+', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='slideshow',
            name='social_image',
            field=models.ForeignKey(related_name=b'core_slideshow_social_image', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the social image will be automatically created from the primary image.', null=True),
        ),
    ]
