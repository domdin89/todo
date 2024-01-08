from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.forms import PasswordInput, TextInput

from .models import Profile
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core import validators
from captcha.fields import CaptchaField

class CaptchaPasswordResetForm(PasswordResetForm):
    pass


class NewResetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=("Nuova Password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=("Enter your DSFDSFADSFSDFSnew password"),
    )
    new_password2 = forms.CharField(
        label=("Conferma nuova password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=("Enter the same password as before, for verification."))

    class Meta:
        fields = ('new_password1', 'new_password2')
        widgets = {
            "new_password1": PasswordInput(attrs={'placeholder':'********','autocomplete': 'off','data-toggle': 'password'}), 
            "new_password2": PasswordInput(attrs={'placeholder':'********','autocomplete': 'off','data-toggle': 'password'}),
        }
    
    def checkPass(new_password1,new_password2):
        print("cipasso")
        if new_password1 != new_password2:
            messages.warning("Le password non coincidono")
            return render('accounts/page-register.html')

class LoginForm(forms.ModelForm):
    username = forms.CharField(label='Username or Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            "username": TextInput(attrs={'placeholder':'ex:test','autocomplete': 'off'}), 
            "password": PasswordInput(attrs={'placeholder':'********','autocomplete': 'off','data-toggle': 'password'}),
        }

