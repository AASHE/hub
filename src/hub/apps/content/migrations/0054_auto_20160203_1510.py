# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tagulous.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0053_auto_20160119_0600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenttype',
            name='keywords',
            field=tagulous.models.fields.TagField(autocomplete_view='tags_autocomplete', to='content._Tagulous_ContentType_keywords', blank=True, help_text='Enter keywords that will be helpful for locating this\n        resource (e.g. "bottled water" for bottled water initiatives).', _set_tag_meta=True, verbose_name='Tags'),
        ),
    ]
