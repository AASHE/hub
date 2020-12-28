# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0061_migrate_created_dates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academicprogram',
            name='founded',
        ),
        migrations.RemoveField(
            model_name='centerandinstitute',
            name='founded',
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='date',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='release_date',
        ),
    ]
