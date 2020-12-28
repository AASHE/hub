# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0049_remove_video_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='cover_image',
        ),
    ]
