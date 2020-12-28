# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0003_delete_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='sustainabilitytopic',
            name='introduction',
            field=models.TextField(null=True, blank=True),
        ),
    ]
