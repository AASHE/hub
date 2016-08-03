# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_initial_choices(apps, schema_editor):
    PublicationMaterialType = apps.get_model('metadata', 'PublicationMaterialType')
    PublicationMaterialType.objects.create(name='Book')
    PublicationMaterialType.objects.create(name='Book Chapter')
    PublicationMaterialType.objects.create(name='Journal Article')
    PublicationMaterialType.objects.create(name='News or Magazine Article')
    PublicationMaterialType.objects.create(name='Blog Article')
    PublicationMaterialType.objects.create(name='Published Report')
    PublicationMaterialType.objects.create(name='Graduate Student Research')
    PublicationMaterialType.objects.create(name='Undergraduate Student Research')


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0019_outreachmaterialtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationMaterialType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Publication Material Type',
                'verbose_name_plural': 'Publication Material Types',
            },
        ),
        migrations.RunPython(create_initial_choices),
    ]
