# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recalls', '0012_auto_20141118_1418'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcategory',
            options={'ordering': ['name'], 'verbose_name_plural': 'Product Categories'},
        ),
        migrations.AlterModelOptions(
            name='productmanufacturer',
            options={'ordering': ['name'], 'verbose_name_plural': 'Product Manufacturers'},
        ),
    ]
