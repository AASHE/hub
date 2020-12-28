# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tagulous.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0051_auto_20160115_2354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contenttype',
            name='keywords',
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='tags',
            field=tagulous.models.fields.TagField(help_text='Enter keywords that will be helpful for locating this\n        resource (e.g. "bottled water" for bottled water initiatives).', to='content._Tagulous_ContentType_tags', _set_tag_meta=True, autocomplete_view='tags_autocomplete', blank=True),
        ),
    ]
