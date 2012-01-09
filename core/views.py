from django.core.serializers import json, serialize
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils import simplejson
from myads.core.decorators import render_template

@render_template
def index(request, template="index.html"):
    return template


class JsonResponse(HttpResponse):
    def __init__(self, object):
        if isinstance(object, QuerySet):
            content = serialize('json', object)
        else:
            content = simplejson.dumps(
                object, indent=2, cls=json.DjangoJSONEncoder,
                ensure_ascii=False)
        super(JsonResponse, self).__init__(
            content, content_type='application/json')