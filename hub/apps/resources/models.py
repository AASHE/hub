from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from feincms.models import Base
from feincms.module.mixins import ContentModelMixin
from model_utils.models import TimeStampedModel

from .content import common

@python_2_unicode_compatible
class Document(TimeStampedModel, ContentModelMixin, Base):

    def __str__(self):
        return str(self.pk)

Document.register_templates({
    'key': 'Default',
    'title': 'Default ',
    'path': 'documents/default.html',
    'regions': (
        ('document', 'Document'),
    ),
})

Document.create_content_type(common.Text, regions=('document',))
