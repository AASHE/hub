# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import feincms.module.mixins
import model_utils.fields
import feincms.extensions


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('template_key', models.CharField(default='Default', max_length=255, verbose_name='template', choices=[('Default', 'Default ')])),
            ],
            options={
                'abstract': False,
            },
            bases=(feincms.module.mixins.ContentModelMixin, models.Model, feincms.extensions.ExtensionsMixin),
        ),
    ]
