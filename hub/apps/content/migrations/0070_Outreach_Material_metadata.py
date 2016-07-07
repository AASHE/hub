# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_material_types(apps, schema_editor):
    OutreachMaterialType = apps.get_model("metadata", "OutreachMaterialType")
    OutreachMaterial = apps.get_model("content", "OutreachMaterial")

    for o in OutreachMaterial.objects.all():
        if o._type == 'flyer':
            o.material_type = OutreachMaterialType.objects.get(id=1)
        elif o._type == 'guide':
            o.material_type = OutreachMaterialType.objects.get(id=2)
        elif o._type == 'infographics':
            o.material_type = OutreachMaterialType.objects.get(id=3)
        elif o._type == 'logo':
            o.material_type = OutreachMaterialType.objects.get(id=4)
        elif o._type == 'map':
            o.material_type = OutreachMaterialType.objects.get(id=5)
        elif o._type == 'other':
            o.material_tyle = OutreachMaterialType.objects.get(id=6)
        elif o._type == 'signs/poster':
            o.material_type = OutreachMaterialType.objects.get(id=7)
        elif o._type == 'sticker':
            o.material_type = OutreachMaterialType.objects.get(id=8)
        o.save()


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0019_outreachmaterialtype'),
        ('content', '0069_Course_Material_metadata'),
    ]

    operations = [
        # Create new field for ForeignKey relation. No need to rename existing field, I don't want to keep the _type
        # name in the end, making new field to conform to conventions used in the other content types instead.
        migrations.AddField(
            model_name='outreachmaterial',
            name='material_type',
            field=models.ForeignKey(verbose_name=b'Type of Material', blank=True, to='metadata.OutreachMaterialType', null=True),
        ),

        # Migrate data over into the new field with ForeignKey lookups
        migrations.RunPython(migrate_material_types),

        # Finally, remove original field
        migrations.RemoveField(
            model_name='outreachmaterial',
            name='_type',
        ),
    ]
