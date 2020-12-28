# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0042_auto_20151211_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='_type',
            field=models.CharField(max_length=40, null=True, verbose_name=b'Type of Material', choices=[(b'book', b'Book'), (b'book chapter', b'Book Chapter'), (b'journal article', b'Journal Article'), (b'news', b'News or Magazine Article'), (b'blog', b'Blog Article'), (b'report', b'Report (Non-Student)'), (b'thesis', b'Student Thesis/Dissertation'), (b'other', b'Other Student Research Paper')]),
        ),
    ]
