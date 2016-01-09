# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0046_auto_20160109_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casestudy',
            name='results',
            field=models.TextField(default='placeholder since this is now required.', help_text=b'Describe the outcomes that resulted\n        from the project implementation.', verbose_name=b'Project Results (or results to date)'),
            preserve_default=False,
        ),
    ]
