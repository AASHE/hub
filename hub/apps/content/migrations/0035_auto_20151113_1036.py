# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0034_auto_20151113_0946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='casestudy',
            name='program_type',
        ),
        migrations.AlterField(
            model_name='video',
            name='link',
            field=models.URLField(default='http://example.com/video.mp4', verbose_name=b'Video Link'),
            preserve_default=False,
        ),
    ]
