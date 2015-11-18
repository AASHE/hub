# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0036_contenttype_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenttype',
            name='published',
            field=models.DateTimeField(help_text='This timestamp is automatically set once the status becomes "Published".', null=True, blank=True),
        ),
    ]
