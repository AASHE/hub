# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0065_migrate_case_study_published_dates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='metadata.Organization', null=True),
        ),
    ]
