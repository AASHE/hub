# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0010_contenttype_featured'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contenttype',
            name='member_only',
        ),
        migrations.AddField(
            model_name='contenttype',
            name='permission',
            field=models.CharField(default=b'member', max_length=20, choices=[(b'open', b'Open - No login Required'), (b'login', b'Public - Login Required'), (b'member', b'Member - AASHE Member Status Required')]),
        ),
    ]
