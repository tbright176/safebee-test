# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0011_auto_20141117_2146'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductManufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name_plural': 'Product Manufacturers',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name_plural': 'Product Categories'},
        ),
        migrations.RemoveField(
            model_name='productrecall',
            name='manufacturers',
        ),
        migrations.AddField(
            model_name='productrecall',
            name='product_manufacturers',
            field=models.ManyToManyField(to='recalls.ProductManufacturer'),
            preserve_default=True,
        ),
    ]
