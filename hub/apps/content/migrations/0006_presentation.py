# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0004_auto_20151012_1314'),
        ('content', '0005_casestudy_centerandinstitute'),
    ]

    operations = [
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('contenttype_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.ContentType')),
                ('date', models.DateField(null=True, blank=True)),
                ('conf_name', models.CharField(blank=True, max_length=100, null=True, choices=[(b'aashe', b'AASHE'), (b'other', b'Other')])),
                ('presentation_type', models.CharField(blank=True, max_length=100, null=True, choices=[(b'poster', b'Poster'), (b'presentation1', b'Presentation (1 speaker)'), (b'presentation2plus', b'Presentation (2 or more speaker)')])),
                ('abstract', models.TextField(null=True, blank=True)),
                ('affirmation', models.BooleanField(default=False, help_text=b"By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted documents in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted image, or have obtained all necessary licenses and/or permissions to use the submitted image, and that AASHE's use of such image will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership')),
                ('institution', models.ForeignKey(blank=True, to='metadata.InstitutionalOffice', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.contenttype',),
        ),
    ]
