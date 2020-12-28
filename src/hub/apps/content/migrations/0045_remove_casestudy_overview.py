# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0044_auto_20151217_2025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='casestudy',
            name='overview',
        ),
    ]
