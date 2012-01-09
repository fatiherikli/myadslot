from django.core.serializers import json, serialize
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson, translation
from core.middleware import LANGUAGE_DOMAIN_PREFIX
from myads.core.decorators import render_template
from django.conf import settings

@render_template
def index(request, template="index.html"):
    language = translation.get_language_from_request(request)
    host = request.META.get("HTTP_HOST")
    if host in settings.NONLOCALE_DOMAINS:
        if language in LANGUAGE_DOMAIN_PREFIX:
            return HttpResponseRedirect(settings.LOCALE_DOMAIN % language)
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