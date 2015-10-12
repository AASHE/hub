# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0003_sustainabilitytopic_color'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sustainabilitytopic',
            options={'ordering': ('color', 'name'), 'verbose_name': 'Sustainability Topic', 'verbose_name_plural': 'Sustainability Topics'},
        ),
    ]
