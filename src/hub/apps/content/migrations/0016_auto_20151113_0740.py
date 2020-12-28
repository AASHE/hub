# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0015_auto_20151113_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenttype',
            name='disciplines',
            field=models.ManyToManyField(to='metadata.AcademicDiscipline', verbose_name='Academic Disciplines'),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='organizations',
            field=models.ManyToManyField(to='metadata.Organization', verbose_name='Organizations'),
        ),
        migrations.AlterField(
            model_name='contenttype',
            name='topics',
            field=models.ManyToManyField(to='metadata.SustainabilityTopic', verbose_name='Sustainability Topics'),
        ),
    ]
