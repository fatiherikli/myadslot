# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class RegistrationForm(forms.Form):
    username = forms.CharField(label=_("Username"))
    first_name = forms.CharField(label=_("First Name"))
    last_name = forms.CharField(label=_("Last Name"))
    email = forms.EmailField()
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use")
        return username

    def clean_email(self):
        username = self.cleaned_data.get("email")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('This email is already in use'))
        return username

    def save(self):
        user = User()
        user.username = self.cleaned_data.get("username")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")
        user.is_active=True
        password = self.cleaned_data.get("password")
        user.set_password(password)
        user.save()


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def authenticate(self, request):
        from django.contrib.auth import authenticate as _authenticate, login as _login
        email = self.data["username"]
        password = self.data["password"]
        user = _authenticate(username=email, password=password)
        _login(request, user)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Email or Password is incorrect.")

        if not user.is_active:
            raise forms.ValidationError("Your membership is not active.")

