# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def copy_dates(apps, schema_editor):
    """
        We want the date created field for case studies, currently not required,
        to mirror the date published field. It will now copy upon saving, but we
        need to copy this data over for existing case study objects.
    """

    CaseStudy = apps.get_model("content", "CaseStudy")
    for c in CaseStudy.objects.all():
        c.date_created = c.published
        c.save()


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0064_auto_20160524_1711'),
    ]

    operations = [
        migrations.RunPython(copy_dates),
    ]
