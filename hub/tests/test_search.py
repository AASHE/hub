from haystack.inputs import Raw
from haystack.query import SearchQuerySet

from ..apps.content.types.academic import AcademicProgram
from .base import BaseSearchBackendTestCase
from ..apps.content.models import Author

TestContentType = AcademicProgram


class SearchBackendTestCase(BaseSearchBackendTestCase):
    """
    Tests around the search backend behavior.
    """


    # first, function that creates a resouce that is publishable

    # second, test if unpublished resource is not indexed (hint: rebuild_index)

    #third, test if published resource is indexed (hint: rebuild_index)
        
