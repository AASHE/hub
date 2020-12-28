# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_auto_20151021_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='document',
            field=models.FileField(help_text=b'The following files formats are acceptable: PDF, Excel, Word, PPT, JPEG, PNG...', null=True, upload_to=b'', blank=True),
        ),
    ]
