# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0023_auto_20151113_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centerandinstitute',
            name='founded',
            field=models.PositiveIntegerField(help_text=b'(e.g. 2009', null=True, verbose_name=b'Year when center or institute was founded', blank=True),
        ),
    ]
