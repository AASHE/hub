# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0002_auto_20151009_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='sustainabilitytopic',
            name='color',
            field=models.CharField(default='#ff0000', max_length=7, verbose_name='HEX Color'),
        ),
    ]
