# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from datetime import date

def move_dates(apps, schema_editor):
    """
        We've added the `date_created` field to the base ContentType, but now
        we need to move the values from several existing models:
            
            AcademicProgram.founded
            CenterAndInstitute.founded
            Presentation.date
            Publication.release_date
    """
    
    AcademicProgram = apps.get_model("content", "AcademicProgram")
    for p in AcademicProgram.objects.all():
        if p.founded:
            p.date_created = date(year=p.founded, month=1, day=1)
            p.save()
    
    CenterAndInstitute = apps.get_model("content", "CenterAndInstitute")
    for c in CenterAndInstitute.objects.all():
        if c.founded:
            c.date_created = date(year=c.founded, month=1, day=1)
            c.save()
    
    Presentation = apps.get_model("content", "Presentation")
    for p in Presentation.objects.all():
        p.date_created = p.date
        p.save()
    
    Publication = apps.get_model("content", "Publication")
    for p in Publication.objects.all():
        p.date_created = p.release_date
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0060_contenttype_date_created'),
    ]

    operations = [
        migrations.RunPython(move_dates),
    ]
