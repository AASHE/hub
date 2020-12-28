# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0009_populate_sustainability_topic_rss_feed'),
    ]

    operations = [
        migrations.AddField(
            model_name='sustainabilitytopic',
            name='css_class',
            field=models.CharField(default='blue', max_length=16, choices=[('blue', 'blue'), ('green', 'green'), ('purple', 'purple'), ('yellow', 'yellow'), ('alt', 'alt')]),
        ),
    ]
