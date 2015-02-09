# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0002_flatpage_modification_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='flatpage',
            name='description',
            field=models.CharField(help_text="This text will be used as the page's meta description for SEO purposes", max_length=150, null=True, blank=True),
            preserve_default=True,
        ),
    ]
