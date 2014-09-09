# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20140710_1427'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': [b'name'], 'verbose_name_plural': b'categories'},
        ),
        migrations.AlterModelOptions(
            name='loopuser',
            options={'ordering': [b'first_name', b'last_name'], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AddField(
            model_name='article',
            name='notes',
            field=models.TextField(help_text=b'For internal notes only.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='slideshow',
            name='notes',
            field=models.TextField(help_text=b'For internal notes only.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.CharField(help_text=b"This text will be used as the content's meta description for SEO purposes", unique=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='article',
            name='teaser',
            field=models.CharField(help_text=b'Optional. If not set, the contents of the description field will be used.', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='slideshow',
            name='description',
            field=models.CharField(help_text=b"This text will be used as the content's meta description for SEO purposes", unique=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='slideshow',
            name='teaser',
            field=models.CharField(help_text=b'Optional. If not set, the contents of the description field will be used.', max_length=255, null=True, blank=True),
        ),
    ]
