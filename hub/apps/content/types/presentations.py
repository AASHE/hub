from django.db import models
from model_utils import Choices

from ..models import ContentType, ContentTypeManager
from ..search import BaseIndex
from ..help import AFFIRMATION, FILE_UPLOAD
from ...metadata.models import ConferenceName, PresentationType


class Presentation(ContentType):

    conf_name = models.ForeignKey(
        ConferenceName, null=True, verbose_name='Conference Name',
        help_text='''If your conference is not listed, please select "other"
        and recommend a change by emailing resources@aashe.org''')
    presentation_type = models.ForeignKey(
        PresentationType, null=True, verbose_name='Presentation Type')

    objects = ContentTypeManager()

    class Meta:
        verbose_name = 'Conference Presentation'
        verbose_name_plural = 'Conference Presentations'

    @classmethod
    def label_overrides(cls):
        return {
            'title': 'Presentation Title',
            'description': 'Description or Abstract',
            'author': 'Presenter',
            'authors': 'Presenters',
            'date_created': 'Presentation Date',
        }
        
    @classmethod
    def required_field_overrides(cls):
        required_list = super(
            Presentation, cls).required_field_overrides()
        required_list.append('date_created')
        return required_list

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import PresentationBrowseFilterSet
        return PresentationBrowseFilterSet

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 0},  # optional, up to 5
            'author': {'max': 6, 'min': 1},  # required, up to 6
            'file': {'max': 3, 'min': 1},  # required, up to 3
            'image': {'max': 5, 'min': 0},  # optional, up to 5
        }


class PresentationIndex(BaseIndex):
    def get_model(self):
        return Presentation
