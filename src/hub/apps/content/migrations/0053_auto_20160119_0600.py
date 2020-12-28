# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0052_auto_20160119_0557'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='_Tagulous_ContentType_tags',
            new_name='_Tagulous_ContentType_keywords',
        ),
        migrations.RenameField(
            model_name='contenttype',
            old_name='tags',
            new_name='keywords',
        ),
    ]
