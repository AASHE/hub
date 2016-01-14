# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0013_sustainabilitytopic_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='sustainabilitytopic',
            name='stars_tab_content',
            field=models.TextField(null=True, blank=True),
        ),
    ]
