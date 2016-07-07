# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_initial_choices(apps, schema_editor):
    OutreachMaterialType = apps.get_model('metadata', 'OutreachMaterialType')
    OutreachMaterialType.objects.create(name='Flyer/Brochure')
    OutreachMaterialType.objects.create(name='Guide')
    OutreachMaterialType.objects.create(name='Infographics')
    OutreachMaterialType.objects.create(name='Logo')
    OutreachMaterialType.objects.create(name='Map')
    OutreachMaterialType.objects.create(name='Other')
    OutreachMaterialType.objects.create(name='Signs/Poster')
    OutreachMaterialType.objects.create(name='Sticker')


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0018_coursematerialtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutreachMaterialType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Outreach Material Type',
                'verbose_name_plural': 'Outreach Material Types',
            },
        ),
        migrations.RunPython(create_initial_choices),
    ]
