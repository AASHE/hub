# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_conference_names_presentation_types(apps, schema_editor):

    Presentation = apps.get_model("content", "Presentation")
    ConferenceName = apps.get_model("metadata", "ConferenceName")
    PresentationType = apps.get_model("metadata", "PresentationType")
    for p in Presentation.objects.all():
        if p.conf_name_archive == 'aashe':
            p.conf_name = ConferenceName.objects.get(id=1)
        else:
            p.conf_name = ConferenceName.objects.get(id=2)
        if p.presentation_type_archive == 'presentation':
            p.presentation_type = PresentationType.objects.get(id=1)
        else:
            p.presentation_type = PresentationType.objects.get(id=2)
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0017_conferencename_presentationtype'),
        ('content', '0066_auto_20160701_2047'),
    ]

    operations = [
        # First rename existing fields to make _archive versions
        migrations.RenameField(
            model_name='presentation',
            old_name='conf_name',
            new_name='conf_name_archive',
        ),
        migrations.RenameField(
            model_name='presentation',
            old_name='presentation_type',
            new_name='presentation_type_archive',
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='date_created',
            field=models.DateField(help_text="Enter the date when this resource was created, founded,\n                                    published, or presented. If you don't know the exact date, choose the\n                                    first day of the month. Use January 1 if you only know the year. You\n                                    can use the calendar widget or type in a date in YYYY-MM-DD format.", null=True, verbose_name='Date Submitted', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='published',
            field=models.DateTimeField(help_text='This timestamp is automatically set once the status becomes "Published".', null=True, verbose_name='Date Published', blank=True),
        ),

        # Create new permanent fields that are ForeignKey relations to the metadata models
        migrations.AddField(
            model_name='presentation',
            name='conf_name',
            field=models.ForeignKey(verbose_name=b'Conference Name', to='metadata.ConferenceName', help_text=b'If your conference is not listed, please select "other"\n        and recommend a change by emailing resources@aashe.org', null=True),
        ),
        migrations.AddField(
            model_name='presentation',
            name='presentation_type',
            field=models.ForeignKey(verbose_name=b'Presentation Type', to='metadata.PresentationType', null=True),
        ),

        # Migrate data over into ForeignKey field
        migrations.RunPython(migrate_conference_names_presentation_types),

        # Finally, remove _archive fields
        migrations.RemoveField(
            model_name='presentation',
            name='conf_name_archive',
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='presentation_type_archive',
        ),
    ]
