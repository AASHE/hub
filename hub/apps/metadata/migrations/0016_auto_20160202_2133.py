# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0015_auto_20160115_2354'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sustainabilitytopicfavorite',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='sustainabilitytopicfavorite',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
