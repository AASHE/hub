# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def populate_rss_feed(apps, schema_editor):
    SustainabilityTopic = apps.get_model("metadata", "SustainabilityTopic")
    for sustainability_topic in SustainabilityTopic.objects.all():
        sustainability_topic.rss_feed = (
            "http://bulletin.aashe.org/rss/news/category/{}".format(
                sustainability_topic.name.lower()))
        sustainability_topic.save()


def empty_rss_feed(apps, schema_editor):
    SustainabilityTopic = apps.get_model("metadata", "SustainabilityTopic")
    for sustainability_topic in SustainabilityTopic.objects.all():
        sustainability_topic.rss_feed = ""
        sustainability_topic.save()


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0008_auto_20151110_1652'),
    ]

    operations = [
        migrations.RunPython(populate_rss_feed,
                             empty_rss_feed)
    ]
