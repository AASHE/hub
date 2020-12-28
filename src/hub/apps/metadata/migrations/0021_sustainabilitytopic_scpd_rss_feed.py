# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_scpd_rss_feed_links(apps, schema_editor):
    SustainabilityTopic = apps.get_model('metadata', 'SustainabilityTopic')
    topics = SustainabilityTopic.objects.all()
    for topic in topics:
        topic.scpd_rss_feed = "http://www.aashe.org/sustainable-campus-partners-directory/rss/sustainability-topic/"\
                            + topic.slug
        topic.save()


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0020_publicationmaterialtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='sustainabilitytopic',
            name='scpd_rss_feed',
            field=models.URLField(null=True, blank=True),
        ),
        # Initialize the new field with links created from the topic slug, then any broken ones can be fixed manually
        # in the admin interface. Faster than creating them all one by one by hand.
        migrations.RunPython(create_scpd_rss_feed_links),
    ]
