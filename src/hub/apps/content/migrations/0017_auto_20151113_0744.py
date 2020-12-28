# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0016_auto_20151113_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenttype',
            name='description',
            field=models.TextField(null=True, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='disciplines',
            field=models.ManyToManyField(to='metadata.AcademicDiscipline', verbose_name='Academic Discipline(s)'),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='keywords',
            field=models.TextField(null=True, verbose_name='Keywords', blank=True),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='organizations',
            field=models.ManyToManyField(to='metadata.Organization', verbose_name='Organization(s)'),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='topics',
            field=models.ManyToManyField(to='metadata.SustainabilityTopic', verbose_name='Sustainability Topic(s)'),
        ),
    ]
