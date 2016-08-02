# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0078_Publication_metadata'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': 'Video / Webinar', 'verbose_name_plural': 'Videos & Webinars'},
        ),
        migrations.AlterField(
            model_name='material',
            name='course_level',
            field=models.CharField(choices=[(b'introductory', b'Introductory'), (b'intermediate', b'Intermediate'), (b'advanced', b'Advanced')], max_length=50, blank=True, help_text=b'100-level courses (or equivalents) may be\n                                    designated as introductory, 200- or 300-level as intermediate, and 400-level or\n                                    graduate courses as advanced.', null=True, verbose_name=b'Course Level'),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='conf_name',
            field=models.ForeignKey(verbose_name=b'Conference Name', to='metadata.ConferenceName', help_text=b'If your conference is not listed, please select "other"\n        and recommend a change by emailing resources@aashe.org', null=True),
        ),
    ]
