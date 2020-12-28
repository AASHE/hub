# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_auto_20151021_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenttype',
            name='published',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contenttype',
            name='status',
            field=models.CharField(default=b'new', max_length=20, choices=[(b'new', b'New'), (b'published', b'Published')]),
        ),
    ]
