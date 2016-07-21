# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def copy_files(apps, schema_editor):
    File = apps.get_model("content", "File")
    for file in File.objects.all():
        try:
            file.item = file.item_archived.url
            file.save()
        except ValueError:  # some may not have associated files
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0072_file_item'),
    ]

    operations = [
        migrations.RunPython(copy_files),
    ]
