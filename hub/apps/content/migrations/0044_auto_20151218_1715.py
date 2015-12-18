# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0043_auto_20151211_2013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='casestudy',
            name='overview',
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='status',
            field=models.CharField(default='new', max_length=20, choices=[('new', 'New'), ('published', 'Published'), ('declined', 'Declined')]),
        ),
        migrations.AlterField(
            model_name='file',
            name='item',
            field=models.FileField(help_text='Valid formats are aceptable: PDF, Excel, Word, PPT...', upload_to=b''),
        ),
        migrations.AlterField(
            model_name='file',
            name='label',
            field=models.CharField(help_text='The title of the document', max_length=100, null=True, blank=True),
        ),
    ]
