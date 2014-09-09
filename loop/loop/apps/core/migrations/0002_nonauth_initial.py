# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('asset_manager', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name=b'last modified', auto_now_add=True)),
                ('status', models.CharField(default=b'D', max_length=1, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled')])),
                ('title', models.CharField(unique=True, max_length=255)),
                ('basename', models.SlugField(help_text=b'By default, this field is auto-generated from the title.', max_length=255)),
                ('subhead', models.CharField(max_length=255, null=True, blank=True)),
                ('teaser', models.CharField(max_length=255, null=True, blank=True)),
                ('canonical_url', models.URLField(help_text=b"Optional. If left blank, the content's auto-generated URL will be used.", null=True, verbose_name=b'Canonical URL', blank=True)),
                ('news_keywords', models.CharField(help_text=b'Enter a comma separated list of keywords (no more than 10) for this page.', max_length=255, null=True, blank=True)),
                ('description', models.CharField(unique=True, max_length=150)),
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
                ('body', models.TextField(null=True, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('primary_image', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', null=True)),
                ('promo_image', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the promo image will be automatically created from the primary image.', null=True)),
                ('social_image', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the social image will be automatically created from the primary image.', null=True)),
            ],
            options={
                'ordering': [b'-publication_date'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('parent', models.ForeignKey(blank=True, to='core.Category', null=True)),
            ],
            options={
                'verbose_name_plural': b'categories',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(to='core.Category'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.TextField(null=True, blank=True)),
                ('order', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', null=True)),
            ],
            options={
                'ordering': [b'order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Slideshow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name=b'last modified', auto_now_add=True)),
                ('status', models.CharField(default=b'D', max_length=1, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled')])),
                ('title', models.CharField(unique=True, max_length=255)),
                ('basename', models.SlugField(help_text=b'By default, this field is auto-generated from the title.', max_length=255)),
                ('subhead', models.CharField(max_length=255, null=True, blank=True)),
                ('teaser', models.CharField(max_length=255, null=True, blank=True)),
                ('canonical_url', models.URLField(help_text=b"Optional. If left blank, the content's auto-generated URL will be used.", null=True, verbose_name=b'Canonical URL', blank=True)),
                ('news_keywords', models.CharField(help_text=b'Enter a comma separated list of keywords (no more than 10) for this page.', max_length=255, null=True, blank=True)),
                ('description', models.CharField(unique=True, max_length=150)),
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
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(to='core.Category')),
                ('primary_image', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', null=True)),
                ('promo_image', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the promo image will be automatically created from the primary image.', null=True)),
                ('social_image', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b'Optional. If left blank, the social image will be automatically created from the primary image.', null=True)),
            ],
            options={
                'ordering': [b'-publication_date'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='slide',
            name='slideshow',
            field=models.ForeignKey(to='core.Slideshow'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='slide',
            unique_together=set([(b'slideshow', b'title')]),
        ),
        migrations.CreateModel(
            name='StreamItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('status', models.CharField(default=b'D', max_length=1, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled')])),
                ('title', models.CharField(max_length=255)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, to='core.Category', null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('promo_image', models.ForeignKey(blank=True, to='asset_manager.Image', null=True)),
            ],
            options={
                'ordering': [b'-publication_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('parent', models.ForeignKey(blank=True, to='core.Tag', null=True)),
            ],
            options={
                'ordering': [b'name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='streamitem',
            name='tags',
            field=models.ManyToManyField(to='core.Tag', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='slideshow',
            name='tags',
            field=models.ManyToManyField(to='core.Tag', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='slideshow',
            unique_together=set([(b'category', b'basename')]),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='core.Tag', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='article',
            unique_together=set([(b'category', b'basename')]),
        ),
    ]
