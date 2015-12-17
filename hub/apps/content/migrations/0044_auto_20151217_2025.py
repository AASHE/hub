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
            name='affirmation',
        ),
        migrations.RemoveField(
            model_name='centerandinstitute',
            name='website',
        ),
        migrations.RemoveField(
            model_name='material',
            name='affirmation',
        ),
        migrations.RemoveField(
            model_name='material',
            name='document',
        ),
        migrations.RemoveField(
            model_name='material',
            name='website',
        ),
        migrations.RemoveField(
            model_name='outreachmaterial',
            name='affirmation',
        ),
        migrations.RemoveField(
            model_name='outreachmaterial',
            name='document',
        ),
        migrations.RemoveField(
            model_name='outreachmaterial',
            name='website',
        ),
        migrations.RemoveField(
            model_name='photograph',
            name='affirmation',
        ),
        migrations.RemoveField(
            model_name='photograph',
            name='caption',
        ),
        migrations.RemoveField(
            model_name='photograph',
            name='credit',
        ),
        migrations.RemoveField(
            model_name='photograph',
            name='image',
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='affirmation',
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='document',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='affirmation',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='document',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='website',
        ),
        migrations.RemoveField(
            model_name='tool',
            name='affirmation',
        ),
        migrations.RemoveField(
            model_name='tool',
            name='document',
        ),
        migrations.RemoveField(
            model_name='tool',
            name='website',
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
