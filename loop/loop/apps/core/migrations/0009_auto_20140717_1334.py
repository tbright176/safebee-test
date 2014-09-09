# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20140714_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.CharField(help_text=b"This text will be used as the content's meta description for SEO purposes", unique=True, max_length=160),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description',
            field=models.CharField(help_text=b'Max 160 characters.', max_length=160, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='slideshow',
            name='description',
            field=models.CharField(help_text=b"This text will be used as the content's meta description for SEO purposes", unique=True, max_length=160),
        ),
        migrations.AlterField(
            model_name='tag',
            name='meta_description',
            field=models.CharField(help_text=b'Max 160 characters.', max_length=160, null=True, blank=True),
        ),
    ]
