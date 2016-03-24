# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0055_auto_20160302_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicprogram',
            name='completion',
            field=models.CharField(help_text=b'(e.g., "2.5 years" or "12 months")', max_length=32, null=True, verbose_name=b'Expected completion time', blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='_type',
            field=models.CharField(help_text=b'"Journal Article," "Graduate Student Research" and\n        "Undergraduate Student Research" submissions will be automatically\n        considered for a Campus Sustainability Research Award as part of\n        AASHE\'s annual awards program.', max_length=40, null=True, verbose_name=b'Type of Material', choices=[(b'book', b'Book'), (b'book chapter', b'Book Chapter'), (b'journal article', b'Journal Article'), (b'news', b'News or Magazine Article'), (b'blog', b'Blog Article'), (b'report', b'Published Report'), (b'graduate', b'Graduate Student Research'), (b'undergrad', b'Undergraduate Student Research')]),
        ),
    ]
