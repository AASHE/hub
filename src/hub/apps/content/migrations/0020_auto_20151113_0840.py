# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0019_auto_20151113_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casestudy',
            name='background',
            field=models.TextField(help_text=b'Describe the circumstances that led to the initiation of\n        this project.', null=True, verbose_name=b'Background', blank=True),
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='financing',
            field=models.TextField(help_text=b'Describe the costs (both upfront and reoccurring) for each\n        component of the project and explain how the project was financed.', null=True, verbose_name=b'Financing', blank=True),
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='goals',
            field=models.TextField(help_text=b'Describe the goals of this project.', null=True, verbose_name=b'Project Goals', blank=True),
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='implementation',
            field=models.TextField(help_text=b'Describe the project and how it was implemented.', null=True, verbose_name=b'Project Implementation', blank=True),
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='institution',
            field=models.ForeignKey(blank=True, to='metadata.InstitutionalOffice', help_text=b'Only include if an office or division on campus is/was\n        directly involved in the case study. Select up to three.', null=True),
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='lessons_learned',
            field=models.TextField(help_text=b'Describe the lessons learned from this project. This\n        section may also be used to offer advice to others who wish to\n        undertake a similar project.', null=True, verbose_name=b'Lessons learned', blank=True),
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='overview',
            field=models.TextField(help_text=b'Provide a very brief summary of your project. Please\n        limit this summary to 100 words.', null=True, verbose_name=b'Project overview', blank=True),
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='results',
            field=models.TextField(help_text=b'Describe the outcomes that resulted\n        from the project implementation.', null=True, verbose_name=b'Project Results (or results to date)', blank=True),
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='timeline',
            field=models.TextField(help_text=b'Describe how long this project took from start to finish\n        and provide a list of key project milestones in chronological order.', null=True, verbose_name=b'Project Timeline', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='keywords',
            field=models.TextField(help_text='Enter keywords that will be helpful for locating this\n        resource (e.g. "bottled water" for bottled water initiatives).', null=True, verbose_name='Keywords', blank=True),
        ),
    ]
