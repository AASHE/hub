# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0045_remove_casestudy_overview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casestudy',
            name='background',
            field=models.TextField(default='placeholder text because this is now required.', help_text=b'Describe the circumstances that led to the initiation of\n        this project.', verbose_name=b'Background'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='financing',
            field=models.TextField(default='placeholder text because this is now required.', help_text=b'Describe the costs (both upfront and reoccurring) for each\n        component of the project and explain how the project was financed.', verbose_name=b'Financing'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='goals',
            field=models.TextField(default='placeholder text because this is now required.', help_text=b'Describe the goals of this project.', verbose_name=b'Project Goals'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='implementation',
            field=models.TextField(default='placeholder text because this is now required.', help_text=b'Describe the project and how it was implemented.', verbose_name=b'Project Implementation'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='lessons_learned',
            field=models.TextField(default='placeholder text because this is now required.', help_text=b'Describe the lessons learned from this project. This\n        section may also be used to offer advice to others who wish to\n        undertake a similar project.', verbose_name=b'Lessons learned'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='casestudy',
            name='timeline',
            field=models.TextField(default='placeholder text because this is now required.', help_text=b'Describe how long this project took from start to finish\n        and provide a list of key project milestones in chronological order.', verbose_name=b'Project Timeline'),
            preserve_default=False,
        ),
    ]
