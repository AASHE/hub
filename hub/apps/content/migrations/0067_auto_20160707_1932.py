# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0066_auto_20160701_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenttype',
            name='date_submitted',
            field=models.DateField(auto_now_add=True, verbose_name='Date Submitted', null=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='date_created',
            field=models.DateField(help_text="Enter the date when this resource was created, founded,\n                                    published, or presented. If you don't know the exact date, choose the\n                                    first day of the month. Use January 1 if you only know the year. You\n                                    can use the calendar widget or type in a date in YYYY-MM-DD format.", null=True, verbose_name='Date Created, Published or Presented', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='published',
            field=models.DateTimeField(help_text='This timestamp is automatically set once the status becomes "Published".', null=True, verbose_name='Date Posted', blank=True),
        ),
    ]
