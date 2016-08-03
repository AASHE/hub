# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0073_copy_old_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='item_archived',
        ),
    ]
