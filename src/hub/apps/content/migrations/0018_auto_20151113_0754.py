# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0017_auto_20151113_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenttype',
            name='disciplines',
            field=models.ManyToManyField(help_text='Select up to three academic disciplines that relate most\n        closely to the academic program.', to='metadata.AcademicDiscipline', verbose_name='Academic Discipline(s)'),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='keywords',
            field=models.TextField(help_text='Enter keywords that provide greater detail on the\n        discipline or will be helpful for locating this resource.', null=True, verbose_name='Keywords', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='organizations',
            field=models.ManyToManyField(help_text=' Select the institution(s) and/or organization(s) that\n        offer(s) this program. If an organization is not on the dropdown list,\n        please complete the new organization form to have it added to our\n        database.', to='metadata.Organization', verbose_name='Organization(s)'),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='topics',
            field=models.ManyToManyField(help_text='Select up to three topics that relate most closely.', to='metadata.SustainabilityTopic', verbose_name='Sustainability Topic(s)'),
        ),
    ]
