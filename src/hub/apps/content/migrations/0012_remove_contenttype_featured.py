# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0011_auto_20151022_1828'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contenttype',
            name='featured',
        ),
    ]
