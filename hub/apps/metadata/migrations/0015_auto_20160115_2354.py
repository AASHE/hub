# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0014_sustainabilitytopic_stars_tab_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sustainabilitytopic',
            name='stars_tab_content',
            field=models.TextField(help_text='Uses Markdown', null=True, blank=True),
        ),
    ]
