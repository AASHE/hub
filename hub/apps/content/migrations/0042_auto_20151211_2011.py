# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0041_auto_20151211_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenttype',
            name='organizations',
            field=models.ManyToManyField(help_text=' Select the institution(s) and/or organization(s) that\n        offer(s) this program. If an organization is not on the dropdown list,\n        please complete the new organization form to have it added to our\n        database.', to='metadata.Organization', verbose_name='Organization(s)', blank=True),
        ),
    ]
