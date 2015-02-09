# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_mostpopularitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='MostPopularRecall',
            fields=[
                ('mostpopularitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='social.MostPopularItem')),
            ],
            options={
            },
            bases=('social.mostpopularitem',),
        ),
    ]
