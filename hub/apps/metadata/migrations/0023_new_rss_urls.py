# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_scpd_rss_feed_links(apps, schema_editor):
    SustainabilityTopic = apps.get_model('metadata', 'SustainabilityTopic')
    topics = SustainabilityTopic.objects.all()
    for topic in topics:
        topic.scpd_rss_feed = "http://partners.aashe.org/rss/sustainability-topic/"\
                            + topic.slug
        topic.save()


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0022_sustainabilitytopic_multiview_zone_id'),
    ]

    operations = [
        # Run create_scpd_rss_feed_links to update the rss URLs now that
        # the SCPD is running on a subdomain partners.aashe.org instead
        # of the old gigantic URL patterns.
        migrations.RunPython(create_scpd_rss_feed_links),
    ]
