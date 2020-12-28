# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0001_initial'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='centerandinstitute',
            name='institution',
            field=models.ForeignKey(blank=True, to='metadata.InstitutionalOffice', null=True),
        ),
    ]
