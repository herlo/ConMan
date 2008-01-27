from common.models import *
from django import newforms as forms

class VolunteerForm(forms.Form):
    vf_objects = list()
    for vf in VolunteerRole.objects.all():
        vf_objects.append((vf.pk,vf.name))
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    title = forms.CharField()
    #role = forms.ChoiceField(vf_objects)
    requested_role = forms.ChoiceField(vf_objects)
    comments = forms.CharField(widget=forms.Textarea,min_length=1,max_length=1000,help_text="Please let us know about any special requests or circumstances.")

class PresenterForm(forms.Form):
    cat_objects = list()
    audience_objects = list()
    for cat in Category.objects.all():
        cat_objects.append((cat.pk,cat.name))
        
    for audience in AudienceType.objects.all():
        audience_objects.append((audience.pk,audience.name))
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    title = forms.CharField()
    category = forms.ChoiceField(cat_objects)
    audience = forms.ChoiceField(audience_objects)
    abstract = forms.CharField(widget=forms.Textarea,min_length=1,max_length=500,help_text="A short abstract less than 500 characters")
    long_abstract = forms.CharField(widget=forms.Textarea,min_length=1,max_length=3000)

vftest = VolunteerForm()
print vftest.as_p()
