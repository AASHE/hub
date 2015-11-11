from json import dumps

from django.http import HttpResponse, HttpResponseBadRequest

from ..metadata.models import Organization

def organizations(request):
    if not request.GET.get('q'):
        return HttpResponseBadRequest('No search term given')
    q = request.GET.get('q')
    data = []
    for o in Organization.objects.values_list('pk', 'org_name') \
                          .filter(org_name__icontains=q):
        data.append({'id': o[0], 'text': o[1]})
    return HttpResponse(dumps(list(data)))
