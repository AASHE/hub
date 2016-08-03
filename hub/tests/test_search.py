from haystack.inputs import Raw
from haystack.query import SearchQuerySet, SQ

from ..apps.content.types.academic import AcademicProgram
from .base import BaseSearchBackendTestCase
from ..apps.content.models import Author

TestContentType = AcademicProgram


class SearchBackendTestCase(BaseSearchBackendTestCase):
    """
    Tests around the search backend behavior.
    """
    def _create_content_item(self, title, published=False, **kwargs):
        status = (
            published and TestContentType.STATUS_CHOICES.published or
            TestContentType.STATUS_CHOICES.new)
        return TestContentType.objects.create(
            title=title, status=status, **kwargs)

    def test_unpublished_item_is_not_indexed(self):
        """
        A content type which is not yet published is not indexed.
        """
        # Create one item, and build the search index
        self._create_content_item('My unpublished item')
        self._rebuild_index()

        # The item is is created, but not in the search backend,
        # since - by default - it's publish status is 'new'.
        self.assertEqual(TestContentType.objects.count(), 1)
        self.assertEqual(SearchQuerySet().all().count(), 0)

    def test_published_item_is_indexed(self):
        """
        A published item is in the search index.
        """
        # Create an object and publish it right away
        self._create_content_item('My published item', True)
        self._rebuild_index()

        # One item is in the search index
        self.assertEqual(TestContentType.objects.count(), 1)
        self.assertEqual(SearchQuerySet().all().count(), 1)

    def test_keyword_matching_behavior(self):
        """
        The search backend should do explict, non-partial keyword matching.
        E.g. for the word Diversity the keywords:

            diver  - do not match
            diver* - do match, because of the star joker

        The search matching should be case-insensitive.
        """
        self._create_content_item('my DIVersiTY item', True)
        self._rebuild_index()

        # One item is in the search index
        self.assertEqual(SearchQuerySet().filter(text=Raw('diver')).count(), 0)
        self.assertEqual(
            SearchQuerySet().filter(text=Raw('diver*')).count(), 1)

    def test_multiple_items_are_properly_indexed(self):
        """
        Multiple items in the search index are properly indexed and found.
        """
        self._create_content_item('my first item', True)
        self._create_content_item('my other first item', True)
        self._create_content_item('my second item', True)
        self._rebuild_index()

        # 'first' only returns two elements
        self.assertEqual(SearchQuerySet().filter(text=Raw('first')).count(), 2)

    def test_keyword_tags_are_properly_indexed(self):
        vid = self._create_content_item(
            'another test item', True)
        vid.keywords.add('figure')

        self._rebuild_index()

        self.assertEqual(SearchQuerySet().filter(
            text=Raw('figure')).count(), 1)

    def test_authors_are_properly_indexed(self):
        vid = self._create_content_item(
            'author test', True)
        tester = Author.objects.create(name='tester', ct=vid)
        vid.authors.add(tester)

        self._rebuild_index()

        self.assertEqual(SearchQuerySet().filter(
            text=Raw('tester')).count(), 1)


class SearchBoostTestCase(BaseSearchBackendTestCase):
    """
    Tests the boosting of results.
    """
    def setUp(self):
        # "Pizza" shows up once in the title
        self.obj1 = TestContentType.objects.create(
                    title="Pizza Toppings",
                    description="Pepperoni, Cheese, Tomatoes",
                    status=TestContentType.STATUS_CHOICES.published)
        # "Pizza" shows up thrice in the description
        self.obj2 = TestContentType.objects.create(
                    title="Food I like",
                    description="Pizza, cheese. Did I mention pizza? Pizza!",
                    status=TestContentType.STATUS_CHOICES.published)
        self.obj2.keywords.add("pizza")
    
    def test_boost(self):
        """
        Confirm that obj1 is of higher rank to obj2
        """
        self._rebuild_index()
        q = "pizza"
        sqs = SearchQuerySet().filter(
            SQ(content=q) | SQ(title=q))
            
        self.assertEqual(sqs[0].pk, "%d" % self.obj1.pk)
