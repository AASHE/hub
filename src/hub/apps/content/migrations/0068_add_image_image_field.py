# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0067_auto_move_image_to_image_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image',
            field=s3direct.fields.S3DirectField(help_text='JPG and PNG file formats are accepted', null=True, blank=True),
        ),
    ]
