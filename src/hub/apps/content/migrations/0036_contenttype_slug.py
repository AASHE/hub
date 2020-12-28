# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from slugify import slugify


def forwards_func(apps, schema_editor):
    """
    Add a slug for every obj in the db so far.
    """
    ContentType = apps.get_model("content", "ContentType")
    db_alias = schema_editor.connection.alias
    for obj in ContentType.objects.using(db_alias).all():
        obj.slug = slugify(obj.title)
        obj.save()

def backwards_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('content', '0035_auto_20151113_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenttype',
            name='slug',
            field=models.CharField(default='slug-not-set-yet', max_length=500, editable=False),
            preserve_default=False,
        ),

        migrations.RunPython(forwards_func, backwards_func)
    ]
