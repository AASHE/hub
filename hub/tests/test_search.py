from django.test import TestCase

from ..apps.content.models import Author, File, Image
from ..apps.content.types.academic import AcademicProgram

TestContentType = AcademicProgram


class SearchBackendTestCase(TestCase):
    """
    Testing the postgres full-text search behavior.
    """
    def _create_ct_item(self, title, published=False, **kwargs):
        status = (
            published and TestContentType.STATUS_CHOICES.published or
            TestContentType.STATUS_CHOICES.new)
        return TestContentType.objects.create(
            title=title, status=status, **kwargs)

    def test_searchvectorfield(self):
        """
        Confirm that search vectors working properly on a ContentType
        """
        ct = self._create_ct_item(
            title='testing', description='these are words')
        ct.refresh_from_db()

        # test the value of the search vector
        self.assertEqual(ct.search_vector, "'test':4 'word':3")
        # test the results of search
        self.assertEqual(
            TestContentType.objects.filter(search_vector='word').count(), 1)
        self.assertEqual(
            TestContentType.objects.filter(search_vector='pizza').count(), 0)

        # Create an Author to trigger the signal and update the vector
        Author.objects.create(name='Jim Smith', ct=ct)
        ct.refresh_from_db()
        self.assertEqual(
            ct.search_vector, "'jim':5 'smith':6 'test':4 'word':3")
        # test search
        self.assertEqual(
            TestContentType.objects.filter(search_vector='smith').count(), 1)

        # Create a File to trigger the signal and update the vector
        File.objects.create(label='My Banana', ct=ct)
        ct.refresh_from_db()
        self.assertEqual(
            ct.search_vector, "'banana':8 'jim':5 'smith':6 'test':4 'word':3")
        # test search
        self.assertEqual(
            TestContentType.objects.filter(search_vector='banana').count(), 1)

        # Create an Image to trigger the signal and update the vector
        Image.objects.create(caption='Sunset', credit='Taylor',
                             med_thumbnail='http://www.x.com/',
                             # small_thumbnail='http://www.y.com/',
                             ct=ct)
        ct.refresh_from_db()
        import ipdb; ipdb.set_trace()
        self.assertEqual(
            ct.search_vector, "'banana':8 'jim':5 'smith':6 'test':4 'word':3")
        # test search
        self.assertEqual(
            TestContentType.objects.filter(search_vector='sunset').count(), 1)
