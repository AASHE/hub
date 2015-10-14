# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.template.defaultfilters import slugify


def set_topic_slugs(apps, schema_editor):
    SustainabilityTopic = apps.get_model('metadata', 'SustainabilityTopic')
    db_alias = schema_editor.connection.alias
    for obj in SustainabilityTopic.objects.using(db_alias).all():
        obj.slug = slugify(obj.name)
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0004_auto_20151012_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='sustainabilitytopic',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),

        migrations.RunPython(set_topic_slugs)
    ]
