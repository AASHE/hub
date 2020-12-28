# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0008_auto_20151110_1652'),
        ('content', '0018_auto_20151113_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicprogram',
            name='institutions',
            field=models.ManyToManyField(help_text=b'Only include if an office or division on campus is directly\n        tied to this academic program. Select up to three.', to='metadata.InstitutionalOffice', verbose_name=b'Institution Office (if relevant)', blank=True),
        ),
        migrations.AlterField(
            model_name='academicprogram',
            name='completion',
            field=models.CharField(help_text=b'(e.g. 2 years and 6 months)', max_length=20, null=True, verbose_name=b'Expected completion time', blank=True),
        ),
        migrations.AlterField(
            model_name='academicprogram',
            name='founded',
            field=models.PositiveIntegerField(help_text=b'(e.g. 2009)', null=True, verbose_name=b'Year Founded', blank=True),
        ),
        migrations.AlterField(
            model_name='academicprogram',
            name='num_students',
            field=models.PositiveIntegerField(help_text=b'We recommend referring to IPEDS data\n        and including an average over five years.', null=True, verbose_name=b'Approximate number of students completing program annually', blank=True),
        ),
        migrations.AlterField(
            model_name='academicprogram',
            name='outcomes',
            field=models.TextField(help_text=b'Consider completing if different from description.', null=True, verbose_name=b'Learning Outcomes', blank=True),
        ),
    ]
