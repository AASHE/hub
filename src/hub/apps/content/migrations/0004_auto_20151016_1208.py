# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20151016_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='document',
            field=models.FileField(help_text=b'The following files formats are acceptable: JPEG, PNG, TIFF...', null=True, upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='outreachmaterial',
            name='document',
            field=models.FileField(help_text=b'The following files formats are acceptable: PDF, Excel, Word, PPT, JPEG, PNG...', null=True, upload_to=b'', blank=True),
        ),
        migrations.AlterField(
            model_name='tool',
            name='document',
            field=models.FileField(help_text=b'The following files formats are acceptable: PDF, Excel, Word, PPT...', null=True, upload_to=b'', blank=True),
        ),
    ]
