# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0008_auto_20151110_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='sustainabilitytopic',
            name='icon',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
    ]
