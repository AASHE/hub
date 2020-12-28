# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0058_auto_20160324_0516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='title',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
