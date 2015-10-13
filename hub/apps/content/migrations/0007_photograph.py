# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0004_auto_20151012_1314'),
        ('content', '0006_presentation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photograph',
            fields=[
                ('contenttype_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.ContentType')),
                ('credit', models.CharField(max_length=500, null=True, blank=True)),
                ('photo', models.ImageField(help_text=b'The following files formats are acceptable: JPEG, PNG, TIFF...', upload_to=b'')),
                ('affirmation', models.BooleanField(default=False)),
                ('institution', models.ForeignKey(blank=True, to='metadata.InstitutionalOffice', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.contenttype',),
        ),
    ]
