# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0005_sustainabilitytopicfavorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='sustainabilitytopic',
            name='rss_feed',
            field=models.URLField(null=True, blank=True),
        ),
    ]
