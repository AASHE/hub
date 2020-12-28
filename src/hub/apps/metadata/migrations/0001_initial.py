# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iss', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicDiscipline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Academic Discipline',
                'verbose_name_plural': 'Academic Disciplines',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='InstitutionalOffice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Institutional Office',
                'verbose_name_plural': 'Institutional Offices',
            },
        ),
        migrations.CreateModel(
            name='ProgramType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Program Type',
                'verbose_name_plural': 'Program Types',
            },
        ),
        migrations.CreateModel(
            name='SustainabilityTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('color', models.CharField(default='#ff0000', max_length=7, verbose_name='HEX Color')),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ('color', 'name'),
                'verbose_name': 'Sustainability Topic',
                'verbose_name_plural': 'Sustainability Topics',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('iss.organization',),
        ),
    ]
