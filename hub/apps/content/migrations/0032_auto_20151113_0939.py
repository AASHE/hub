# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0008_auto_20151110_1652'),
        ('content', '0031_auto_20151113_0930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tool',
            name='institution',
        ),
        migrations.RemoveField(
            model_name='video',
            name='affirmation',
        ),
        migrations.RemoveField(
            model_name='video',
            name='institution',
        ),
        migrations.AddField(
            model_name='material',
            name='institutions',
            field=models.ManyToManyField(help_text=b'Only include if an office or division on campus is/was\n        directly involved in the case study. Select up to three.', to='metadata.InstitutionalOffice', verbose_name=b'Institution Office (if relevant)', blank=True),
        ),
        migrations.AddField(
            model_name='tool',
            name='website',
            field=models.URLField(null=True, verbose_name=b'Website', blank=True),
        ),
        migrations.AlterField(
            model_name='tool',
            name='document',
            field=models.FileField(help_text=b'The following files formats are acceptable: PDF, Excel, Word, PPT... Provide either a\n        website or a publication document.', upload_to=b'', null=True, verbose_name=b'Document Upload', blank=True),
        ),
    ]
