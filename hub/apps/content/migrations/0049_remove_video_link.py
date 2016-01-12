# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0048_rename_content_types'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='link',
        ),
    ]
