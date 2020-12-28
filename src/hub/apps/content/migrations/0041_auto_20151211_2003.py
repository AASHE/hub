# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0040_auto_20151211_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentation',
            name='presentation_type',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'poster', b'Poster'), (b'presentation', b'Presentation')]),
        ),
    ]
