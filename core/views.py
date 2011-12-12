from django.shortcuts import render_to_response
from django.template.context import RequestContext

def index(request, template="index.html"):
    return render_to_response("index.html", context_instance=RequestContext(request))


