# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='academicdiscipline',
            options={'ordering': ('name',), 'verbose_name': 'Academic Discipline', 'verbose_name_plural': 'Academic Disciplines'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('name',), 'verbose_name': 'Country', 'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='institutionaloffice',
            options={'ordering': ('name',), 'verbose_name': 'Institutional Office', 'verbose_name_plural': 'Institutional Offices'},
        ),
        migrations.AlterModelOptions(
            name='programtype',
            options={'ordering': ('name',), 'verbose_name': 'Program Type', 'verbose_name_plural': 'Program Types'},
        ),
        migrations.AlterModelOptions(
            name='sustainabilitytopic',
            options={'ordering': ('name',), 'verbose_name': 'Sustainability Topic', 'verbose_name_plural': 'Sustainability Topics'},
        ),
    ]
