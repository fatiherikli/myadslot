# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from auth.forms import RegistrationForm, LoginForm
from django.contrib.auth import logout as _logout
from core.decorators import render_template

def logout(request):
    _logout(request)
    return HttpResponseRedirect("/")

@render_template
def login(request, template="auth/login.html"):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("dashboard"))

    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            form.authenticate(request)

            # previous page
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET["next"])
            return HttpResponseRedirect(reverse('dashboard'))


    ctx = {
        "form" : form
    }
    return template, ctx

@render_template
def register(request, template="auth/register.html"):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth_complete'))

    ctx = {
        "form" : form
    }
    return template, ctx

@render_template
def complete(request, template="auth/complete.html"):
    return template