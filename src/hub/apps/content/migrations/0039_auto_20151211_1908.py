# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0038_contenttype_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicprogram',
            name='program_type',
            field=models.ForeignKey(verbose_name=b'Program Type', to='metadata.ProgramType', null=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='disciplines',
            field=models.ManyToManyField(help_text='Select up to three academic disciplines that relate most\n        closely to the academic program.', to='metadata.AcademicDiscipline', verbose_name='Academic Discipline(s)', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='institutions',
            field=models.ManyToManyField(help_text='Only include if an office or division on campus is/was\n        directly involved in the case study. Select up to three.', to='metadata.InstitutionalOffice', verbose_name='Office or Department', blank=True),
        ),
    ]
