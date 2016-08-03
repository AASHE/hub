# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0070_remove_image_image_archived'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='item',
            new_name='item_archived',
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='topics',
            field=models.ManyToManyField(help_text='Select up to three topics that relate most closely to\n        this resource.', to='metadata.SustainabilityTopic', verbose_name='Sustainability Topic(s)'),
        ),
    ]
