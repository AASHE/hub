# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0033_auto_20151113_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='outreachmaterial',
            name='_type',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name=b'Type of Material', choices=[(b'logo', b'Logo'), (b'signs/poster', b'Signs/Poster'), (b'sticker', b'Sticker'), (b'flyer', b'Flyer/Brochure'), (b'guide', b'Guide'), (b'map', b'Map'), (b'other', b'Other')]),
        ),
        migrations.AddField(
            model_name='outreachmaterial',
            name='website',
            field=models.URLField(null=True, verbose_name=b'Website', blank=True),
        ),
        migrations.AlterField(
            model_name='outreachmaterial',
            name='design_credit',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Design credit (name and/or organization)', blank=True),
        ),
        migrations.AlterField(
            model_name='outreachmaterial',
            name='document',
            field=models.FileField(help_text=b'The following files formats are acceptable: PDF, Excel, Word, PPT... Provide either a\n        website or a publication document.', upload_to=b'', null=True, verbose_name=b'Document Upload', blank=True),
        ),
    ]
