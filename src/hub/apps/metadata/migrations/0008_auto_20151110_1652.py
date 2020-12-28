# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0007_auto_20151110_1522'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sustainabilitytopic',
            options={'ordering': ('order', 'name'), 'verbose_name': 'Sustainability Topic', 'verbose_name_plural': 'Sustainability Topics'},
        ),
        migrations.AddField(
            model_name='sustainabilitytopic',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
