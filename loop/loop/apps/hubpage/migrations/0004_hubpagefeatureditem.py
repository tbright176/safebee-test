# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_photoblog_intro'),
        ('hubpage', '0003_contentmodule_hide_featured_story_byline'),
    ]

    operations = [
        migrations.CreateModel(
            name='HubPageFeaturedItem',
            fields=[
                ('relateditem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.RelatedItem')),
                ('layout', models.CharField(default=b'D', max_length=2, choices=[(b'D', b'Default'), (b'P', b'Poll')])),
                ('hide_title_and_description', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('core.relateditem',),
        ),
    ]
