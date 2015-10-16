# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_centerandinstitute_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photograph',
            name='photo',
            field=models.ImageField(help_text=b'The following files formats are acceptable: JPEG, PNG, TIFF...', null=True, upload_to=b'', blank=True),
        ),
    ]
