# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0001_initial'),
        ('iss', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('is_author', models.BooleanField(default=False, verbose_name=b'I am an author')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('content_type', models.CharField(max_length=40, choices=[(b'academicprogram', b'Academic Program'), (b'casestudy', b'Case Study'), (b'center', b'Research Center & Institute'), (b'presentation', b'Conference Presentation'), (b'publication', b'Publication'), (b'photograph', b'Photograph'), (b'course', b'Course Material'), (b'tool', b'Tool'), (b'video', b'Video'), (b'outreach', b'Outreach Material')])),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField(null=True, blank=True)),
                ('keywords', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Genric Content Type',
                'verbose_name_plural': '- All Content Types -',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('label', models.CharField(max_length=100, null=True, blank=True)),
                ('_file', models.FileField(help_text=b'The following files formats are aceptable: PDF, Excel, Word, PPT...', null=True, upload_to=b'', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('caption', models.CharField(max_length=500, null=True, blank=True)),
                ('credit', models.CharField(max_length=500, null=True, blank=True)),
                ('image', models.ImageField(help_text=b'The following files formats are acceptable: JPEG, PNG, TIFF...', upload_to=b'')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('label', models.CharField(max_length=100, null=True, blank=True)),
                ('url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AcademicProgram',
            fields=[
                ('contenttype_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.ContentType')),
                ('outcomes', models.TextField(null=True, verbose_name=b'Learning Outcomes', blank=True)),
                ('founded', models.PositiveIntegerField(null=True, blank=True)),
                ('completion', models.CharField(max_length=20, null=True, verbose_name=b'Expected completion time', blank=True)),
                ('num_students', models.PositiveIntegerField(null=True, verbose_name=b'Approximate number of students completing program annually', blank=True)),
                ('distance', models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Distance Education', choices=[(b'local', b'Local Only'), (b'distance', b'Distance Education'), (b'both', b'Both')])),
                ('commitment', models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Commitment', choices=[(b'full', b'Full-Time'), (b'part', b'Part-Time'), (b'both', b'Both')])),
                ('program_type', models.ForeignKey(verbose_name=b'Program Type', blank=True, to='metadata.ProgramType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.contenttype',),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('contenttype_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.ContentType')),
                ('release_date', models.DateField(null=True, blank=True)),
                ('publisher', models.CharField(max_length=200, null=True, blank=True)),
                ('periodical_name', models.CharField(max_length=200, null=True, blank=True)),
                ('_type', models.CharField(blank=True, max_length=40, null=True, verbose_name=b'Type of Material', choices=[(b'book', b'Book'), (b'book chapter', b'Book Chapter'), (b'journal article', b'Journal Article'), (b'news', b'News or Magazine Article'), (b'blog', b'Blog Article'), (b'report', b'Report (Non-Student)'), (b'thesis', b'Student Thesis/Dissertation'), (b'other', b'Other Student Research Paper')])),
                ('cover_image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('affirmation', models.BooleanField(default=False)),
                ('institution', models.ForeignKey(blank=True, to='metadata.InstitutionalOffice', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('content.contenttype',),
        ),
        migrations.AddField(
            model_name='website',
            name='ct',
            field=models.ForeignKey(to='content.ContentType'),
        ),
        migrations.AddField(
            model_name='image',
            name='ct',
            field=models.ForeignKey(to='content.ContentType'),
        ),
        migrations.AddField(
            model_name='file',
            name='ct',
            field=models.ForeignKey(to='content.ContentType'),
        ),
        migrations.AddField(
            model_name='contenttype',
            name='disciplines',
            field=models.ManyToManyField(to='metadata.AcademicDiscipline', verbose_name=b'Academic Disciplines', blank=True),
        ),
        migrations.AddField(
            model_name='contenttype',
            name='organizations',
            field=models.ManyToManyField(to='iss.Organization', verbose_name=b'Organizations', blank=True),
        ),
        migrations.AddField(
            model_name='contenttype',
            name='topics',
            field=models.ManyToManyField(to='metadata.SustainabilityTopic', verbose_name=b'Sustainability Topics', blank=True),
        ),
        migrations.AddField(
            model_name='author',
            name='ct',
            field=models.ForeignKey(to='content.ContentType'),
        ),
        migrations.AddField(
            model_name='author',
            name='organization',
            field=models.ForeignKey(blank=True, to='iss.Organization', null=True),
        ),
    ]
