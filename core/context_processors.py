from django.conf import settings
from auth.forms import LoginForm


def myads_general(request):
    return {
        "login_form" : LoginForm(),
    }