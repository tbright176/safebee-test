# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20140917_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled')]),
        ),
        migrations.AlterField(
            model_name='infographic',
            name='status',
            field=models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled')]),
        ),
        migrations.AlterField(
            model_name='photoblog',
            name='status',
            field=models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled')]),
        ),
        migrations.AlterField(
            model_name='photooftheday',
            name='status',
            field=models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled')]),
        ),
        migrations.AlterField(
            model_name='slideshow',
            name='status',
            field=models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled')]),
        ),
        migrations.AlterField(
            model_name='streamitem',
            name='status',
            field=models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled')]),
        ),
        migrations.AlterField(
            model_name='tipslist',
            name='status',
            field=models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Draft'), (b'M', b'Moderate'), (b'P', b'Published'), (b'S', b'Scheduled')]),
        ),
    ]
