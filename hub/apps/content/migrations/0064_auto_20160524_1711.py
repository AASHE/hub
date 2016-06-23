# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0063_auto_20160513_1349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='slug',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
