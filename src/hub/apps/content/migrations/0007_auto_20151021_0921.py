# -*- coding: utf-8 -*-

"""

    Update all existing content types to be published.

"""

from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone

def forwards_func(apps, schema_editor):
    ContentType = apps.get_model("content", "ContentType")
    db_alias = schema_editor.connection.alias
    ContentType.objects.using(db_alias).update(status='published',
        published=timezone.now())

def backwards_func(apps, schema_editor):
    ContentType = apps.get_model("content", "ContentType")
    db_alias = schema_editor.connection.alias
    ContentType.objects.using(db_alias).update(status='new', published=None)


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_auto_20151021_0920'),
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func)
    ]
