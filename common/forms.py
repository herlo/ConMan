from common.models import *
from django import newforms as forms
from django.newforms import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ContactUsForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'autoexpandbox'}))
    captcha_text = forms.CharField()
    captcha_uid = forms.CharField(widget=forms.HiddenInput())
