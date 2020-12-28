# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0011_topic_hex_to_css'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sustainabilitytopic',
            name='color',
        ),
        migrations.AlterField(
            model_name='sustainabilitytopic',
            name='css_class',
            field=models.CharField(default='blue', max_length=16, choices=[('blue', 'blue'), ('lightblue', 'lightblue'), ('green', 'green'), ('purple', 'purple'), ('lightpurple', 'lightpurple'), ('yellow', 'yellow'), ('alt', 'alt')]),
        ),
    ]
