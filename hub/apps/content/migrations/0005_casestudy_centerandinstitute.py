# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0004_auto_20151012_1314'),
        ('content', '0004_auto_20151012_1314'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseStudy',
            fields=[
                ('contenttype_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.ContentType')),
                ('overview', models.TextField(null=True, verbose_name=b'Project overview', blank=True)),
                ('background', models.TextField(null=True, verbose_name=b'Background', blank=True)),
                ('goals', models.TextField(null=True, verbose_name=b'Project Goals', blank=True)),
                ('implementation', models.TextField(null=True, verbose_name=b'Project Implementation', blank=True)),
                ('timeline', models.TextField(null=True, verbose_name=b'Project Timeline', blank=True)),
                ('financing', models.TextField(null=True, verbose_name=b'Financing', blank=True)),
                ('results', models.TextField(null=True, verbose_name=b'Project Results (or results to date)', blank=True)),
                ('lessons_learned', models.TextField(null=True, verbose_name=b'Lessons learned', blank=True)),
                ('affirmation', models.BooleanField(default=False, help_text=b"By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted documents in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted image, or have obtained all necessary licenses and/or permissions to use the submitted image, and that AASHE's use of such image will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership')),
                ('institution', models.ForeignKey(blank=True, to='metadata.InstitutionalOffice', null=True)),
                ('program_type', models.ForeignKey(verbose_name=b'Program Type', blank=True, to='metadata.ProgramType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.contenttype',),
        ),
        migrations.CreateModel(
            name='CenterAndInstitute',
            fields=[
                ('contenttype_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.ContentType')),
                ('num_paid', models.PositiveIntegerField(null=True, verbose_name=b'Number of Paid Staff', blank=True)),
                ('founded', models.PositiveIntegerField(null=True, verbose_name=b'Year Founded', blank=True)),
                ('budget', models.PositiveIntegerField(null=True, verbose_name=b'Total Budget', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.contenttype',),
        ),
    ]
