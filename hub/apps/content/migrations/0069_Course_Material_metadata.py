# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_material_types(apps, schema_editor):

    CourseMaterialType = apps.get_model("metadata", "CourseMaterialType")
    Material = apps.get_model("content", "Material")

    for m in Material.objects.all():
        if m.material_type_archive == 'assignment':
            m.material_type = CourseMaterialType.objects.get(id=1)
        elif m.material_type_archive == 'syllabus':
            m.material_type = CourseMaterialType.objects.get(id=2)
        else:
            m.material_type = CourseMaterialType.objects.get(id=3)
        m.save()


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0018_coursematerialtype'),
        ('content', '0068_Presentation_metadata'),
    ]

    operations = [
        # First rename existing field to make _archive version
        migrations.RenameField(
            model_name='material',
            old_name='material_type',
            new_name='material_type_archive',
        ),

        # Create a permanent field with original name that is ForeignKey relationship with new metadata class
        migrations.AddField(
            model_name='material',
            name='material_type',
            field=models.ForeignKey(to='metadata.CourseMaterialType', help_text=b'Select the best option.', null=True, verbose_name=b'Type of Material'),
        ),

        # Migrate data over into ForeignKey field
        migrations.RunPython(migrate_material_types),

        # Finally, remove _archive field
        migrations.RemoveField(
            model_name='material',
            name='material_type_archive',
        ),
    ]
