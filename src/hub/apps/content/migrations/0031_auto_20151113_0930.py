# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0030_auto_20151113_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='material_type',
            field=models.CharField(default='course', help_text=b'Select the best option.', max_length=50, verbose_name=b'Type of Material', choices=[(b'assignment', b'Assignment or Exercise'), (b'syllabus', b'Syllabus'), (b'course', b'Course Presentation')]),
            preserve_default=False,
        ),
    ]
