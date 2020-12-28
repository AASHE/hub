# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0008_auto_20151110_1652'),
        ('content', '0027_auto_20151113_0911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photograph',
            name='institution',
        ),
        migrations.RemoveField(
            model_name='photograph',
            name='photo',
        ),
        migrations.AddField(
            model_name='photograph',
            name='caption',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Caption description', blank=True),
        ),
        migrations.AddField(
            model_name='photograph',
            name='image',
            field=models.ImageField(default='/file-does-not-exist/', help_text=b'The following files formats are acceptable: JPEG, PNG, TIFF...', upload_to=b''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photograph',
            name='institutions',
            field=models.ManyToManyField(help_text=b'Only include if an office or division on campus is/was\n        directly involved in the case study. Select up to three.', to='metadata.InstitutionalOffice', verbose_name=b'Institution Office (if relevant)', blank=True),
        ),
        migrations.AlterField(
            model_name='photograph',
            name='credit',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Photographer credit (name and/or organization', blank=True),
        ),
    ]
