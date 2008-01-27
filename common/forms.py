from common.models import *
from django import newforms as forms

class VolunteerForm(forms.Form):
    firstname = forms.CharField()
    lastname = forms.CharField()
    email = forms.EmailField()
    title = forms.CharField()
    role = forms.ChoiceField(role)
    req = forms.CharField()
    comments = forms.CharField()

class PresenterForm(forms.Form):
    firstname = forms.CharField()
    lastname = forms.CharField()
    email = forms.EmailField()
    title = forms.CharField()
    category = forms.ChoiceField(categories)
    audience = forms.ChoiceField(audiences)
    abstract = forms.CharField()
    longabstract = forms.CharField()

