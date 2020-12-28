# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0025_auto_20151113_0848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presentation',
            name='abstract',
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='institution',
        ),
        migrations.AlterField(
            model_name='presentation',
            name='conf_name',
            field=models.CharField(default='other', max_length=100, verbose_name=b'Conference Name', choices=[(b'aashe', b'AASHE'), (b'other', b'Other')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='presentation',
            name='date',
            field=models.DateField(default=datetime.date(2015, 11, 13), verbose_name=b'Presentation Date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='presentation',
            name='document',
            field=models.FileField(help_text=b'The following files formats are acceptable: PDF, Excel, Word, PPT...', upload_to=b'', null=True, verbose_name=b'Document Upload', blank=True),
        ),
    ]
