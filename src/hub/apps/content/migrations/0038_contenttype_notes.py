# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0037_auto_20151118_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenttype',
            name='notes',
            field=models.TextField(default='', help_text='Internal notes.', null=True, verbose_name='Notes', blank=True),
        ),
    ]
