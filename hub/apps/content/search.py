from haystack import indexes

class BaseIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Base Haystack index class for each content type index. We don't use much
    features of a search engine, we only index a blob of text, to search against,
    and the actual content type primary key, which we later use to filter
    down a queryset of content types.
    """
    text = indexes.CharField(document=True, use_template=True)
    ct_pk = indexes.IntegerField()

    def prepare_ct_pk(self, obj):
        """
        Save the actual primary key of the base content type object along the
        index row. We need those later to filter a queryset.
        """
        from .models import CONTENT_TYPES
        ct_name = CONTENT_TYPES[obj.content_type]._meta.model_name.lower()
        return getattr(obj, ct_name).pk

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            status=self.get_model().STATUS_CHOICES.published)

    def get_model(self):
        raise NotImplementedError
