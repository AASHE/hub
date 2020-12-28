# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0008_auto_20151110_1652'),
        ('content', '0020_auto_20151113_0840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='casestudy',
            name='institution',
        ),
        migrations.AddField(
            model_name='casestudy',
            name='institution',
            field=models.ManyToManyField(help_text=b'Only include if an office or division on campus is/was\n        directly involved in the case study. Select up to three.', to='metadata.InstitutionalOffice', blank=True),
        ),
    ]
