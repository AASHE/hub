# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_auto_20151021_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenttype',
            name='member_only',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='ct',
            field=models.ForeignKey(related_name='authors', to='content.ContentType'),
        ),
        migrations.AlterField(
            model_name='file',
            name='ct',
            field=models.ForeignKey(related_name='files', to='content.ContentType'),
        ),
        migrations.AlterField(
            model_name='image',
            name='ct',
            field=models.ForeignKey(related_name='images', to='content.ContentType'),
        ),
        migrations.AlterField(
            model_name='website',
            name='ct',
            field=models.ForeignKey(related_name='websites', to='content.ContentType'),
        ),
    ]
