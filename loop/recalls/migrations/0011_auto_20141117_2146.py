# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0010_recallsnstopic'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='productrecall',
            name='product_types',
        ),
        migrations.AddField(
            model_name='productrecall',
            name='product_categories',
            field=models.ManyToManyField(to='recalls.ProductCategory'),
            preserve_default=True,
        ),
    ]
