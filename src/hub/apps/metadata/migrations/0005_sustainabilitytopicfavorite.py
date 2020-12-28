# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_remove_contenttype_featured'),
        ('metadata', '0004_sustainabilitytopic_introduction'),
    ]

    operations = [
        migrations.CreateModel(
            name='SustainabilityTopicFavorite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('ct', models.ForeignKey(verbose_name='Content Type', to='content.ContentType')),
                ('topic', models.ForeignKey(verbose_name='Sustainability Topic', to='metadata.SustainabilityTopic')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
