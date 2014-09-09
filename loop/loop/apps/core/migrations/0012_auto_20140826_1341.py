# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20140814_1842'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photooftheday',
            options={'ordering': [b'-publication_date'], 'verbose_name': b'Photo of the Day', 'verbose_name_plural': b'Photos of the Day'},
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Draft'), (b'M0', b'Moderate 0'), (b'M1', b'Moderate 1'), (b'M2', b'Moderate 2'), (b'F', b'Final Review'), (b'R', b'Ready for Pub'), (b'P', b'Published'), (b'S', b'Scheduled'), (b'T', b'Trash')]),
        ),
        migrations.AlterField(
            model_name='photooftheday',
            name='status',
            field=models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Draft'), (b'M0', b'Moderate 0'), (b'M1', b'Moderate 1'), (b'M2', b'Moderate 2'), (b'F', b'Final Review'), (b'R', b'Ready for Pub'), (b'P', b'Published'), (b'S', b'Scheduled'), (b'T', b'Trash')]),
        ),
        migrations.AlterField(
            model_name='slideshow',
            name='status',
            field=models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Draft'), (b'M0', b'Moderate 0'), (b'M1', b'Moderate 1'), (b'M2', b'Moderate 2'), (b'F', b'Final Review'), (b'R', b'Ready for Pub'), (b'P', b'Published'), (b'S', b'Scheduled'), (b'T', b'Trash')]),
        ),
        migrations.AlterField(
            model_name='streamitem',
            name='status',
            field=models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Draft'), (b'M0', b'Moderate 0'), (b'M1', b'Moderate 1'), (b'M2', b'Moderate 2'), (b'F', b'Final Review'), (b'R', b'Ready for Pub'), (b'P', b'Published'), (b'S', b'Scheduled'), (b'T', b'Trash')]),
        ),
    ]
