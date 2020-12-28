from linkcheck import Linklist
from apps.content.models import Website, Image
from apps.metadata.models import SustainabilityTopic


class WebsiteLinkList(Linklist):
    model = Website
    url_fields = ['url']


class ImageLinkList(Linklist):
    model = Image
    image_fields = ['image']


class SustainabilityTopicLinklist(Linklist):
    model = SustainabilityTopic
    url_fields = ['rss_feed']
    html_fields = ['stars_tab_content']


linklists = {'Websites': WebsiteLinkList,
             'Images': ImageLinkList,
             'Sustainability Topics': SustainabilityTopicLinklist}
