# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0022_auto_20151113_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='centerandinstitute',
            name='website',
            field=models.URLField(default='http://example.com/', verbose_name=b'Website'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='centerandinstitute',
            name='budget',
            field=models.PositiveIntegerField(help_text=b'in U.S. dollars', null=True, verbose_name=b'Total operating budget for the center or institute (excluding salaries)?', blank=True),
        ),
        migrations.AlterField(
            model_name='centerandinstitute',
            name='founded',
            field=models.PositiveIntegerField(null=True, verbose_name=b'Year when center or institute was founded', blank=True),
        ),
        migrations.AlterField(
            model_name='centerandinstitute',
            name='num_paid',
            field=models.PositiveIntegerField(null=True, verbose_name=b'Number of paid staff employed at the center (FTE)', blank=True),
        ),
    ]
