# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def update_presentation_types(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Presentation = apps.get_model("content", "Presentation")
    for p in Presentation.objects.all():
        if(
            p.presentation_type == "presentation1" or
            p.presentation_type == "presentation2plus"
        ):
            p.presentation_type = "presentation"
            p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0039_auto_20151211_1908'),
    ]

    operations = [
        migrations.RunPython(update_presentation_types),
    ]
