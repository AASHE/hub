# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def hex_to_styles(apps, schema_editor):
    SustainabilityTopic = apps.get_model("metadata", "SustainabilityTopic")
    mapping = (
        ('#00bce4', 'lightblue'),
        ('#a486bd', 'lightpurple'),
        ('#15387f', 'blue'),
        ('#6bbc49', 'lightgreen')
    )
    for topic in SustainabilityTopic.objects.all():
        for m in mapping:
            if topic.color == m[0]:
                topic.css_class = m[1]
                topic.save()
                print topic
                print topic.css_class
                print topic.color
                break


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0010_sustainabilitytopic_css_class'),
    ]

    operations = [
        migrations.RunPython(hex_to_styles),
    ]
