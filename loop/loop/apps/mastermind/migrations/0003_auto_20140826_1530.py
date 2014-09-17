# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0002_auto_20140826_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='basename',
            field=models.SlugField(default='', help_text=b'By default, this field is auto-generated from the title.', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='canonical_url',
            field=models.URLField(help_text=b"Optional. If left blank, the content's auto-generated URL will be used.", null=True, verbose_name=b'Canonical URL', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='creation_date',
            field=models.DateTimeField(default=datetime.date(2014, 8, 26), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='disable_comments',
            field=models.BooleanField(default=False, help_text=b'Check to disable comments on this piece of content.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='enable_standout_tag',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='exclude_from_home_page',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='exclude_from_newsletter_rss',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='exclude_from_rss',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='exclude_from_sitemap',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='exclude_from_twitter',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='hide_right_rail',
            field=models.BooleanField(default=False, help_text=b'Check to hide the right rail on this page.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='modification_date',
            field=models.DateTimeField(default=datetime.date(2014, 8, 26), auto_now=True, auto_now_add=True, verbose_name=b'last modified'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='news_keywords',
            field=models.CharField(help_text=b'Enter a comma separated list of keywords (no more than 10) for this page.', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='nofollow',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='noindex',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='noodp_noydir',
            field=models.BooleanField(default=True, verbose_name=b'NOODP/NOYDIR'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='notes',
            field=models.TextField(help_text=b'For internal notes only.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='page_title',
            field=models.CharField(help_text=b"Optional. Use this to customize the title displayed in the page's &lt;title&gt; tag.", max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='primary_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='promo_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the promo image will be automatically created from the primary image.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='publication_date',
            field=models.DateTimeField(default=django.utils.timezone.now, db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='social_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the social image will be automatically created from the primary image.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='status',
            field=models.CharField(default=b'D', max_length=1, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled'), (b'T', b'Trash')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='subhead',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='tags',
            field=models.ManyToManyField(to=b'core.Tag', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='teaser',
            field=models.CharField(help_text=b'Optional. If not set, the contents of the description field will be used.', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='background_image',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='slug',
        ),
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.CharField(help_text=b"This text will be used as the content's meta description for SEO purposes", unique=True, max_length=160),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
