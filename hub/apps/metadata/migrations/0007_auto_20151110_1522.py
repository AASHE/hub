# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0006_sustainabilitytopic_rss_feed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sustainabilitytopic',
            options={'ordering': ('name',), 'verbose_name': 'Sustainability Topic', 'verbose_name_plural': 'Sustainability Topics'},
        ),
    ]
