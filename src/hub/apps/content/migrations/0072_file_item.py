# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0071_auto_20160714_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='item',
            field=s3direct.fields.S3DirectField(help_text='Valid formats are aceptable: PDF, Excel, Word, PPT', null=True, blank=True),
        ),
    ]
