# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0029_auto_20151113_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='website',
            field=models.URLField(null=True, verbose_name=b'Website', blank=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='course_level',
            field=models.CharField(choices=[(b'introductory', b'Introductory'), (b'intermediate', b'Intermediate'), (b'advanced', b'Advanced')], max_length=50, blank=True, help_text=b'e.g. 100-level courses may be\n        designated as introductory, 200-300 for intermediate, 400-level for\n        advanced, or similar structures', null=True, verbose_name=b'Course Level'),
        ),
        migrations.AlterField(
            model_name='material',
            name='course_name',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Course Name', blank=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='document',
            field=models.FileField(help_text=b'The following files formats are acceptable: PDF, Excel, Word, PPT... Provide either a\n        website or a publication document.', upload_to=b'', null=True, verbose_name=b'Document Upload', blank=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='material_type',
            field=models.CharField(choices=[(b'assignment', b'Assignment or Exercise'), (b'syllabus', b'Syllabus'), (b'course', b'Course Presentation')], max_length=50, blank=True, help_text=b'Select the best option.', null=True, verbose_name=b'Type of Material'),
        ),
    ]
