# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_material_types(apps, schema_editor):
    PublicationMaterialType = apps.get_model("metadata", "PublicationMaterialType")
    Publication = apps.get_model("content", "Publication")

    for p in Publication.objects.all():
        if p._type == 'book':
            p.material_type = PublicationMaterialType.objects.get(id=1)
        elif p._type == 'book chapter':
            p.material_type = PublicationMaterialType.objects.get(id=2)
        elif p._type == 'journal article':
            p.material_type = PublicationMaterialType.objects.get(id=3)
        elif p._type == 'news':
            p.material_type = PublicationMaterialType.objects.get(id=4)
        elif p._type == 'blog':
            p.material_type = PublicationMaterialType.objects.get(id=5)
        elif p._type == 'report':
            p.material_type = PublicationMaterialType.objects.get(id=6)
        elif p._type == 'graduate':
            p.material_type = PublicationMaterialType.objects.get(id=7)
        elif p._type == 'undergrad':
            p.material_type = PublicationMaterialType.objects.get(id=8)
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0020_publicationmaterialtype'),
        ('content', '0077_Outreach_Material_metadata'),
    ]

    operations = [
        # Add new ForeignKey field
        migrations.AddField(
            model_name='publication',
            name='material_type',
            field=models.ForeignKey(verbose_name=b'Type of Material', to='metadata.PublicationMaterialType', help_text=b'"Journal Article," "Graduate Student Research" and\n        "Undergraduate Student Research" submissions will be automatically\n        considered for a Campus Sustainability Research Award as part of\n        AASHE\'s annual awards program.', null=True),
        ),

        # Migrate data to new field using ForeignKey lookups
        migrations.RunPython(migrate_material_types),

        # Delete original field
        migrations.RemoveField(
            model_name='publication',
            name='_type',
        ),
    ]
