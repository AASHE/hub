# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0028_auto_20151113_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photograph',
            name='image',
            field=models.ImageField(help_text=b'The following files formats are acceptable: JPEG, GIF, PNG...', upload_to=b''),
        ),
    ]
