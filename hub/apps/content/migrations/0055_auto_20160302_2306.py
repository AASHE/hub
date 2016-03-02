# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tagulous.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0054_auto_20160203_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='casestudy',
            name='consider_for_award',
            field=models.BooleanField(default=False, help_text=b'Would you like this case study to be considered for an\n        AASHE Student Leadership Award? The first author must be a student.', verbose_name=b'Student Leadership Award'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='academicprogram',
            name='completion',
            field=models.CharField(help_text=b'(e.g., "2.5 years" or "12 months")', max_length=20, null=True, verbose_name=b'Expected completion time', blank=True),
        ),
        migrations.AlterField(
            model_name='academicprogram',
            name='founded',
            field=models.PositiveIntegerField(help_text=b'Enter a four digit year (e.g., 2009)', null=True, verbose_name=b'Year Founded', blank=True),
        ),
        migrations.AlterField(
            model_name='academicprogram',
            name='num_students',
            field=models.PositiveIntegerField(help_text=b'Enter student headcounts instead of\n        FTE. We recommend referring to Integrated Postsecondary Education Data\n        System (IPEDS) data and including an average over five years.', null=True, verbose_name=b'Approximate number of students completing program annually', blank=True),
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='background',
            field=models.TextField(help_text=b'Describe the circumstances that led to start-up of this\n        project.', verbose_name=b'Background'),
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='financing',
            field=models.TextField(help_text=b'Describe the costs (both upfront and recurring) for each\n        component of the project and explain how the project was financed.', verbose_name=b'Financing'),
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='implementation',
            field=models.TextField(help_text=b'Describe how the project was implemented, including who\n        was involved.', verbose_name=b'Project Implementation'),
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='lessons_learned',
            field=models.TextField(help_text=b'Describe what you learned though this project that would\n        be helpful to others wishing to undertake a similar project.', verbose_name=b'Lessons learned'),
        ),
        migrations.AlterField(
            model_name='centerandinstitute',
            name='founded',
            field=models.PositiveIntegerField(help_text=b'Enter a four digit year (e.g., 2009)', null=True, verbose_name=b'Year when center or institute was founded', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='disciplines',
            field=models.ManyToManyField(help_text='Only include if an academic discipline is directly tied to\n        this resource (select up to three).', to='metadata.AcademicDiscipline', verbose_name='Academic Discipline(s)', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='institutions',
            field=models.ManyToManyField(help_text='Only include if an office or division on campus is\n        directly tied to this resource (select up to three).', to='metadata.InstitutionalOffice', verbose_name='Office(s) or Department(s)', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='keywords',
            field=tagulous.models.fields.TagField(autocomplete_view='tags_autocomplete', to='content._Tagulous_ContentType_keywords', blank=True, help_text='Enter keywords that will be helpful for grouping this\n        resource (e.g. "bottled water" for bottled water initiatives). For\n        multiple tags, use comma or return as separator.', _set_tag_meta=True, verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='organizations',
            field=models.ManyToManyField(help_text='Select the institution(s) and/or organization(s) that are\n        directly tied to this resource. If an organization is not on the\n        dropdown list, please contact resources@aashe.org.', to='metadata.Organization', verbose_name='Organization(s)', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='topics',
            field=models.ManyToManyField(help_text='Select up to three topics that relate most closely to \n        this resource.', to='metadata.SustainabilityTopic', verbose_name='Sustainability Topic(s)'),
        ),
        migrations.AlterField(
            model_name='image',
            name='credit',
            field=models.CharField(max_length=500, null=True, verbose_name='Photographer credit', blank=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='course_level',
            field=models.CharField(choices=[(b'introductory', b'Introductory'), (b'intermediate', b'Intermediate'), (b'advanced', b'Advanced')], max_length=50, blank=True, help_text=b'100-level courses (or equivalents)\n        may be designated as introductory, 200- or 300-level as intermediate,\n        and 400-level or graduate courses as advanced.', null=True, verbose_name=b'Course Level'),
        ),
        migrations.AlterField(
            model_name='outreachmaterial',
            name='_type',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name=b'Type of Material', choices=[(b'flyer', b'Flyer/Brochure'), (b'guide', b'Guide'), (b'infographics', b'Infographics'), (b'logo', b'Logo'), (b'map', b'Map'), (b'other', b'Other'), (b'signs/poster', b'Signs/Poster'), (b'sticker', b'Sticker')]),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='conf_name',
            field=models.CharField(help_text=b'If your conference is not\n        listed, please select "other" and recommend a change by emailing\n        resources@aashe.org', max_length=100, verbose_name=b'Conference Name', choices=[(b'aashe', b'AASHE'), (b'other', b'Other')]),
        ),
        migrations.AlterField(
            model_name='presentation',
            name='date',
            field=models.DateField(help_text=b"If you don't know\n    the exact day, choose the first day of the month. Use January 1 if you only\n    know the year. You can use the calendar widget or type in a date in\n    YYYY-MM-DD format.", verbose_name=b'Presentation Date'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='_type',
            field=models.CharField(help_text=b'"Graduate Student Research" or "Undergraduate Student\n        Research" submissions will be considered for AASHE\'s Annual Student\n        Research Award.', max_length=40, null=True, verbose_name=b'Type of Material', choices=[(b'book', b'Book'), (b'book chapter', b'Book Chapter'), (b'journal article', b'Journal Article'), (b'news', b'News or Magazine Article'), (b'blog', b'Blog Article'), (b'report', b'Report (Non-Student)'), (b'thesis', b'Student Thesis/Dissertation'), (b'other', b'Other Student Research Paper')]),
        ),
        migrations.AlterField(
            model_name='publication',
            name='release_date',
            field=models.DateField(help_text=b"If you don't know the exact day,\n        choose the first day of the month. Use January 1 if you only know the\n        year. You can use the calendar widget or type in a date in YYYY-MM-DD\n        format.", null=True, verbose_name=b'Publication release date', blank=True),
        ),
    ]
