# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_initial_choices(apps, schema_editor):
    CourseMaterialType = apps.get_model('metadata', 'CourseMaterialType')
    CourseMaterialType.objects.create(name='Assignment or Exercise')
    CourseMaterialType.objects.create(name='Syllabus')
    CourseMaterialType.objects.create(name='Course Presentation')


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0017_conferencename_presentationtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseMaterialType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Course Material Type',
                'verbose_name_plural': 'Course Material Types',
            },
        ),
        migrations.RunPython(create_initial_choices),
    ]
