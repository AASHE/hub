# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_photograph'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('contenttype_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.ContentType')),
                ('document', models.FileField(help_text=b'The following files formats are acceptable: JPEG, PNG, TIFF...', upload_to=b'')),
                ('material_type', models.CharField(blank=True, max_length=50, null=True, choices=[(b'assignment', b'Assignment or Exercise'), (b'syllabus', b'Syllabus'), (b'course', b'Course Presentation')])),
                ('course_name', models.CharField(max_length=500, null=True, blank=True)),
                ('course_level', models.CharField(blank=True, max_length=50, null=True, choices=[(b'introductory', b'Introductory'), (b'intermediate', b'Intermediate'), (b'advanced', b'Advanced')])),
                ('affirmation', models.BooleanField(default=False, help_text=b"By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted documents in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted image, or have obtained all necessary licenses and/or permissions to use the submitted image, and that AASHE's use of such image will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership')),
            ],
            options={
                'abstract': False,
            },
            bases=('content.contenttype',),
        ),
    ]
