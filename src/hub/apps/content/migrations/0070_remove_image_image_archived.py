# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0069_copy_old_images_to_new'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image_archived',
        ),
    ]
