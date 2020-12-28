# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0059_auto_20160325_0547'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenttype',
            name='date_created',
            field=models.DateField(help_text="\n        Enter the date when this resource was created, founded, published, or\n        presented. If you don't know the exact date, choose the first day of\n        the month. Use January 1 if you only know the year. You can use the\n        calendar widget or type in a date in YYYY-MM-DD format.", null=True, blank=True),
        ),
    ]
