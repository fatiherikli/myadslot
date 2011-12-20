from django.shortcuts import render_to_response
from core.decorators import render_template

@render_template
def index(request, template="index.html"):
    return template
