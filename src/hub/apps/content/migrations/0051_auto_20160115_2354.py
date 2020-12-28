# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tagulous.models.fields
import tagulous.models.models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0050_remove_publication_cover_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='_Tagulous_ContentType_tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='_tagulous_contenttype_tags',
            unique_together=set([('slug',)]),
        ),
        migrations.AddField(
            model_name='contenttype',
            name='tags',
            field=tagulous.models.fields.TagField(help_text='Enter a comma-separated tag string', to='content._Tagulous_ContentType_tags', autocomplete_view='tags_autocomplete', _set_tag_meta=True),
        ),
    ]
