# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_remove_contenttype_program_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicprogram',
            name='_type',
            field=models.ForeignKey(verbose_name=b'Program Type', blank=True, to='metadata.ProgramType', null=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='content_type',
            field=models.CharField(max_length=40, choices=[(b'academicprogram', b'Academic Program'), (b'casestudy', b'Case Study'), (b'center', b'Research Center & Institute'), (b'presentation', b'Conference Presentation'), (b'publication', b'Publication'), (b'photograph', b'Photograph'), (b'course', b'Course Material'), (b'tool', b'Tool'), (b'video', b'Video'), (b'outreach', b'Outreach Material')]),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='disciplines',
            field=models.ManyToManyField(to='metadata.AcademicDiscipline', verbose_name=b'Academic Disciplines', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='organizations',
            field=models.ManyToManyField(to='issdjango.Organizations', verbose_name=b'Organizations', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='topics',
            field=models.ManyToManyField(to='metadata.SustainabilityTopic', verbose_name=b'Sustainability Topics', blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='_type',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name=b'Type of Material', choices=[(b'book', b'Book'), (b'book chapter', b'Book Chapter'), (b'journal article', b'Journal Article'), (b'news', b'News or Magazine Article'), (b'blog', b'Blog Article'), (b'report', b'Report (Non-Student)'), (b'thesis', b'Student Thesis/Dissertation'), (b'other', b'Other Student Research Paper')]),
        ),
    ]
