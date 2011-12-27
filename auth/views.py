from django.contrib.auth import logout as _logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from auth.forms import ProfileEditForm
from myads.auth.decorators import login_required
from myads.auth.forms import RegistrationForm, LoginForm
from myads.core.decorators import render_template
from myads.auth.forms import PasswordChangeForm

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
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("dashboard"))

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

@login_required
@render_template
def change_password(request, template="auth/change_password.html"):
    form = PasswordChangeForm(request.user)
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data["new_password2"])
            request.user.save()

    return template, {
        "form" : form
    }


@login_required
@render_template
def update_profile(request, template="auth/update_profile.html"):
    form = ProfileEditForm(instance=request.user)
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

    return template, {
        "form" : form
    }

@render_template
def complete(request, template="auth/complete.html"):
    return template