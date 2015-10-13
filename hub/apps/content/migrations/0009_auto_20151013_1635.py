# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0004_auto_20151012_1314'),
        ('content', '0008_material'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutreachMaterial',
            fields=[
                ('contenttype_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.ContentType')),
                ('document', models.FileField(help_text=b'The following files formats are acceptable: PDF, Excel, Word, PPT, JPEG, PNG...', upload_to=b'')),
                ('design_credit', models.CharField(max_length=500, null=True, blank=True)),
                ('affirmation', models.BooleanField(default=False, help_text=b"By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted documents in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted image, or have obtained all necessary licenses and/or permissions to use the submitted image, and that AASHE's use of such image will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership')),
                ('institution', models.ForeignKey(blank=True, to='metadata.InstitutionalOffice', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.contenttype',),
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('contenttype_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.ContentType')),
                ('document', models.FileField(help_text=b'The following files formats are acceptable: PDF, Excel, Word, PPT...', upload_to=b'')),
                ('affirmation', models.BooleanField(default=False, help_text=b"By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted documents in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted image, or have obtained all necessary licenses and/or permissions to use the submitted image, and that AASHE's use of such image will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership')),
                ('institution', models.ForeignKey(blank=True, to='metadata.InstitutionalOffice', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.contenttype',),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('contenttype_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.ContentType')),
                ('link', models.URLField(null=True, verbose_name=b'Video Link', blank=True)),
                ('affirmation', models.BooleanField(default=False, help_text=b"By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted documents in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted image, or have obtained all necessary licenses and/or permissions to use the submitted image, and that AASHE's use of such image will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership')),
                ('institution', models.ForeignKey(blank=True, to='metadata.InstitutionalOffice', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.contenttype',),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='content_type',
            field=models.CharField(max_length=40, choices=[(b'academicprogram', b'Academic Program'), (b'casestudy', b'Case Study'), (b'center', b'Research Center & Institute'), (b'presentation', b'Conference Presentation'), (b'publication', b'Publication'), (b'photograph', b'Photograph'), (b'material', b'Course Material'), (b'tool', b'Tool'), (b'video', b'Video'), (b'outreach', b'Outreach Material')]),
        ),
        migrations.AlterField(
            model_name='photograph',
            name='affirmation',
            field=models.BooleanField(default=False, help_text=b"By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted documents in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted image, or have obtained all necessary licenses and/or permissions to use the submitted image, and that AASHE's use of such image will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='affirmation',
            field=models.BooleanField(default=False, help_text=b"By checking this box, you are granting AASHE an irrevocable, royalty-free, non-exclusive and perpetual license to use the submitted documents in publications, newsletters, resources or promotional materials, and you are hereby representing and warranting that you own all the rights to the submitted image, or have obtained all necessary licenses and/or permissions to use the submitted image, and that AASHE's use of such image will not infringe the rights of any third party, including but not limited to intellectual property rights, or any other rights protected by law (such as the right to privacy or right of publicity).", verbose_name=b'Affirmation of Ownership'),
        ),
    ]
