# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0012_auto_20160106_0323'),
    ]

    operations = [
        migrations.AddField(
            model_name='sustainabilitytopic',
            name='icon',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
    ]
