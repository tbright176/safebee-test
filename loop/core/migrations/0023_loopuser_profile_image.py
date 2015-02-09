# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20140919_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='loopuser',
            name='profile_image',
            field=models.ImageField(help_text=b'Image should be large, preferably 640x640 or larger. Please ensure the photo will work well in a square aspect ratio.', null=True, upload_to=b'profiles', blank=True),
            preserve_default=True,
        ),
    ]
