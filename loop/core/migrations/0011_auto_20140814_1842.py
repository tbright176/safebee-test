# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asset_manager', '__first__'),
        ('core', '0010_article_primary_image_caption_override'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoOfTheDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name=b'last modified', auto_now_add=True)),
                ('status', models.CharField(default=b'D', max_length=1, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled'), (b'T', b'Trash')])),
                ('title', models.CharField(unique=True, max_length=255)),
                ('basename', models.SlugField(help_text=b'By default, this field is auto-generated from the title.', max_length=255)),
                ('subhead', models.CharField(max_length=255, null=True, blank=True)),
                ('teaser', models.CharField(help_text=b'Optional. If not set, the contents of the description field will be used.', max_length=255, null=True, blank=True)),
                ('notes', models.TextField(help_text=b'For internal notes only.', null=True, blank=True)),
                ('canonical_url', models.URLField(help_text=b"Optional. If left blank, the content's auto-generated URL will be used.", null=True, verbose_name=b'Canonical URL', blank=True)),
                ('news_keywords', models.CharField(help_text=b'Enter a comma separated list of keywords (no more than 10) for this page.', max_length=255, null=True, blank=True)),
                ('description', models.CharField(help_text=b"This text will be used as the content's meta description for SEO purposes", unique=True, max_length=160)),
                ('enable_standout_tag', models.BooleanField(default=False)),
                ('noodp_noydir', models.BooleanField(default=True, verbose_name=b'NOODP/NOYDIR')),
                ('nofollow', models.BooleanField(default=False)),
                ('noindex', models.BooleanField(default=False)),
                ('page_title', models.CharField(help_text=b"Optional. Use this to customize the title displayed in the page's &lt;title&gt; tag.", max_length=255, null=True, blank=True)),
                ('exclude_from_home_page', models.BooleanField(default=False)),
                ('exclude_from_rss', models.BooleanField(default=False)),
                ('exclude_from_newsletter_rss', models.BooleanField(default=False)),
                ('exclude_from_twitter', models.BooleanField(default=False)),
                ('exclude_from_sitemap', models.BooleanField(default=False)),
                ('disable_comments', models.BooleanField(default=False, help_text=b'Check to disable comments on this piece of content.')),
                ('hide_right_rail', models.BooleanField(default=False, help_text=b'Check to hide the right rail on this page.')),
                ('subtitle', models.CharField(max_length=255, null=True, blank=True)),
                ('caption', models.TextField(null=True, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(to='core.Category')),
                ('primary_image', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', null=True)),
                ('promo_image', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the promo image will be automatically created from the primary image.', null=True)),
                ('social_image', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the social image will be automatically created from the primary image.', null=True)),
                ('tags', models.ManyToManyField(to='core.Tag', null=True, blank=True)),
            ],
            options={
                'ordering': [b'-publication_date'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='photooftheday',
            unique_together=set([(b'category', b'basename')]),
        ),
    ]
