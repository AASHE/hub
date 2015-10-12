# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20151009_1136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='academicprogram',
            old_name='_type',
            new_name='program_type',
        ),
    ]
