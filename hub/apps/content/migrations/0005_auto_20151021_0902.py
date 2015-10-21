# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_auto_20151016_1208'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='academicprogram',
            options={'verbose_name': 'Academic Program', 'verbose_name_plural': 'Academic Programs'},
        ),
        migrations.AlterModelOptions(
            name='casestudy',
            options={'verbose_name': 'Case Study', 'verbose_name_plural': 'Case Studies'},
        ),
        migrations.AlterModelOptions(
            name='centerandinstitute',
            options={'verbose_name': 'Research Center & Institute', 'verbose_name_plural': 'Research Centers & Institutes'},
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'verbose_name': 'Course Material', 'verbose_name_plural': 'Course Materials'},
        ),
        migrations.AlterModelOptions(
            name='outreachmaterial',
            options={'verbose_name': 'Outreach Material', 'verbose_name_plural': 'Outreach Materials'},
        ),
        migrations.AlterModelOptions(
            name='photograph',
            options={'verbose_name': 'Photograph', 'verbose_name_plural': 'Photographs'},
        ),
        migrations.AlterModelOptions(
            name='presentation',
            options={'verbose_name': 'Conference Presentation', 'verbose_name_plural': 'Conference Presentations'},
        ),
        migrations.AlterModelOptions(
            name='publication',
            options={'verbose_name': 'Publication', 'verbose_name_plural': 'Publications'},
        ),
        migrations.AlterModelOptions(
            name='tool',
            options={'verbose_name': 'Tool', 'verbose_name_plural': 'Tools'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': 'Video', 'verbose_name_plural': 'Videos'},
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='content_type',
            field=models.CharField(max_length=40),
        ),
    ]
