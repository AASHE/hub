# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0008_auto_20151110_1652'),
        ('content', '0021_auto_20151113_0841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='casestudy',
            name='institution',
        ),
        migrations.RemoveField(
            model_name='centerandinstitute',
            name='institution',
        ),
        migrations.AddField(
            model_name='casestudy',
            name='institutions',
            field=models.ManyToManyField(help_text=b'Only include if an office or division on campus is/was\n        directly involved in the case study. Select up to three.', to='metadata.InstitutionalOffice', verbose_name=b'Institution Office (if relevant)', blank=True),
        ),
        migrations.AddField(
            model_name='centerandinstitute',
            name='institutions',
            field=models.ManyToManyField(help_text=b'Only include if an office or division on campus is/was\n        directly involved in the case study. Select up to three.', to='metadata.InstitutionalOffice', verbose_name=b'Institution Office (if relevant)', blank=True),
        ),
        migrations.AlterField(
            model_name='academicprogram',
            name='institutions',
            field=models.ManyToManyField(help_text=b'Only include if an office or division on campus is/was\n        directly involved in the case study. Select up to three.', to='metadata.InstitutionalOffice', verbose_name=b'Institution Office (if relevant)', blank=True),
        ),
    ]
