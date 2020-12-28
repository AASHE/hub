# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0062_auto_20160502_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenttype',
            name='description',
            field=models.TextField(help_text='Styling with\n        <a href="https://simplemde.com/markdown-guide" target="_blank">Markdown</a>\n        is supported', null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='slug',
            field=models.CharField(max_length=500),
        ),
    ]
