# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    """
        outreach >> outreachmaterial
        center >> centerandinstitute
    """

    def rename_content_types(apps, schema_editor):
        OutreachMaterial = apps.get_model("content", "OutreachMaterial")
        CenterAndInstitute = apps.get_model("content", "CenterAndInstitute")

        for om in OutreachMaterial.objects.all():
            om.content_type = 'outreachmaterial'
            om.save()

        for ci in CenterAndInstitute.objects.all():
            ci.content_type = 'centerandinstitute'
            ci.save()

    dependencies = [
        ('content', '0047_auto_20160109_0158'),
    ]

    operations = [
        migrations.RunPython(rename_content_types),
    ]
