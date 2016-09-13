from django_filters.widgets import LinkWidget
from django.utils.encoding import force_text
from django.db.models.fields import BLANK_CHOICE_DASH


class GalleryViewWidget(LinkWidget):
    """
    Custom LinkWidget for the gallery view
    """

    def option_string(self):
        return '''
            <li%(attrs)s><a class="btn btn-default" href="?%(query_string)s">
            <i class="fa fa-%(label)s pull-right"></i></a></li>'''
