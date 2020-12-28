# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0008_auto_20151110_1652'),
        ('content', '0026_auto_20151113_0859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='institution',
        ),
        migrations.AddField(
            model_name='publication',
            name='document',
            field=models.FileField(help_text=b'The following files formats are acceptable: PDF, Excel, Word, PPT... Provide either a\n        website or a publication document.', upload_to=b'', null=True, verbose_name=b'Document Upload', blank=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='institutions',
            field=models.ManyToManyField(help_text=b'Only include if an office or division on campus is/was\n        directly involved in the case study. Select up to three.', to='metadata.InstitutionalOffice', verbose_name=b'Institution Office (if relevant)', blank=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='website',
            field=models.URLField(null=True, verbose_name=b'Website', blank=True),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='presentation_type',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'poster', b'Poster'), (b'presentation1', b'Presentation (1 speaker)'), (b'presentation2plus', b'Presentation (2 or more speakers)')]),
        ),
        migrations.AlterField(
            model_name='publication',
            name='cover_image',
            field=models.ImageField(help_text=b'The following files formats are acceptable: JPEG, GIF, PNG...', null=True, upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='periodical_name',
            field=models.CharField(help_text=b'Enter the name of\n        the periodical (e.g., journal, magazine, newspaper), if applicable. For\n        book chapers, enter the title of the book.', max_length=200, null=True, verbose_name=b'Periodical/publication name', blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publisher',
            field=models.CharField(help_text=b'Enter the name of the publisher, if applicable.', max_length=200, null=True, verbose_name=b'Publisher', blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='release_date',
            field=models.DateField(help_text=b'Providing a release date is\n        highly recommended.', null=True, verbose_name=b'Publication release date', blank=True),
        ),
    ]
