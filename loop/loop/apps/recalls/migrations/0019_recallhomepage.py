# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset_manager', '0004_auto_20140910_1544'),
        ('recalls', '0018_ulpublicnotice'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecallHomePage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('featured_recall_title', models.CharField(help_text=b"Override the featured recall's title.", max_length=255, null=True, blank=True)),
                ('featured_recall_url', models.URLField(help_text=b"Override the featured recall's URL.", null=True, blank=True)),
                ('featured_recall_issue_description', models.CharField(help_text=b"A short description of the type of hazard involved in the recall, e.g. 'Issue: Strangulation Hazard'.", max_length=255, null=True, blank=True)),
                ('featured_recall', models.ForeignKey(blank=True, to='recalls.RecallStreamItem', null=True)),
                ('featured_recall_image', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='asset_manager.Image', help_text=b"Set the featured recall's image. The size should be at least 780x391.", null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
