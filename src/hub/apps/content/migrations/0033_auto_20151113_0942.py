# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0008_auto_20151110_1652'),
        ('content', '0032_auto_20151113_0939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academicprogram',
            name='institutions',
        ),
        migrations.RemoveField(
            model_name='casestudy',
            name='institutions',
        ),
        migrations.RemoveField(
            model_name='centerandinstitute',
            name='institutions',
        ),
        migrations.RemoveField(
            model_name='material',
            name='institutions',
        ),
        migrations.RemoveField(
            model_name='outreachmaterial',
            name='institution',
        ),
        migrations.RemoveField(
            model_name='photograph',
            name='institutions',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='institutions',
        ),
        migrations.AddField(
            model_name='contenttype',
            name='institutions',
            field=models.ManyToManyField(help_text='Only include if an office or division on campus is/was\n        directly involved in the case study. Select up to three.', to='metadata.InstitutionalOffice', verbose_name='Institution Office (if relevant)', blank=True),
        ),
    ]
