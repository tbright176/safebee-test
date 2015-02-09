# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('show_title', models.BooleanField(default=False, help_text=b'Show title bar above module')),
                ('body', models.TextField()),
                ('active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('url', models.CharField(help_text=b"Use an absolute path without the domain name, e.g. /food-health/this-is-the-basename.html. If using a category path, like '/food-health/', be sure to include the trailing slash.", unique=True, max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RailItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(null=True, blank=True)),
                ('module', models.ForeignKey(to='rail_manager.Module', to_field='id')),
                ('rail', models.ForeignKey(to='rail_manager.Rail', to_field='id')),
            ],
            options={
                'ordering': (b'order',),
            },
            bases=(models.Model,),
        ),
    ]
