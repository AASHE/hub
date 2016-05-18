from django.conf import settings
from datetime import datetime

def cache_vars(request):
    return {
        'CACHE_TTL_LONG': settings.CACHE_TTL_LONG,
        'CACHE_TTL_SHORT': settings.CACHE_TTL_SHORT,
    }
