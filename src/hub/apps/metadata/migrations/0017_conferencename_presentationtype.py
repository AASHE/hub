# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_initial_choices(apps, schema_editor):

    ConferenceName = apps.get_model('metadata', 'ConferenceName')
    ConferenceName.objects.create(name='AASHE')
    ConferenceName.objects.create(name='Other')

    PresentationType = apps.get_model('metadata', 'PresentationType')
    PresentationType.objects.create(name='Presentation')
    PresentationType.objects.create(name='Poster')


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0016_auto_20160202_2133'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Conference Name',
                'verbose_name_plural': 'Conference Names',
            },
        ),
        migrations.CreateModel(
            name='PresentationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Presentation Type',
                'verbose_name_plural': 'Presentation Types',
            },
        ),
        migrations.RunPython(create_initial_choices)
    ]
