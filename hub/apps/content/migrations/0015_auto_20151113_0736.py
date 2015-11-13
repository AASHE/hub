# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0014_auto_20151110_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='is_author',
        ),
        migrations.AlterField(
            model_name='file',
            name='item',
            field=models.FileField(default='/file-does-not-exist-due-db-migration/', help_text='The following files formats are aceptable: PDF, Excel, Word, PPT...', upload_to=b''),
            preserve_default=False,
        ),
    ]
