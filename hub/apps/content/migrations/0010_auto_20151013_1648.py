# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_auto_20151013_1635'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'verbose_name': 'Additional File', 'verbose_name_plural': 'Additional Files'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Additional Image', 'verbose_name_plural': 'Additional Images'},
        ),
        migrations.RenameField(
            model_name='file',
            old_name='_file',
            new_name='item',
        ),
        migrations.AddField(
            model_name='file',
            name='affirmation',
            field=models.BooleanField(default=False, verbose_name=b'Affirmation of Ownership'),
        ),
    ]
