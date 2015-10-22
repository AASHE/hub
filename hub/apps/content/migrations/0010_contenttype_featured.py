# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_presentation_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenttype',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
