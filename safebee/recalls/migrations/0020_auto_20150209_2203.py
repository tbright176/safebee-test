# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0019_recallhomepage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recallhomepage',
            options={'verbose_name_plural': 'recall home page'},
        ),
        migrations.AlterModelOptions(
            name='recallstreamitem',
            options={'ordering': ['-recall_date']},
        ),
        migrations.AlterField(
            model_name='recallhomepage',
            name='featured_recall_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b"REQUIRED. Set the featured recall's image. The size should be at least 780x391.", null=True),
            preserve_default=True,
        ),
    ]
