from common.models import *
from django import newforms as forms
from django.newforms import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class VolunteerForm(forms.Form):
    vf_objects = list()
    shirt_objects = list()
    for vf in VolunteerRole.objects.all():
        vf_objects.append((vf.pk,vf.name))
    
    for ss in ShirtSize.objects.all():
        shirt_objects.append((ss.pk,ss.name))
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput,min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput,min_length=6)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    job_title = forms.CharField(required=False)
    irc_nick = forms.CharField(label="IRC Nickname", required=False)
    irc_server = forms.CharField(label="IRC Server", required=False)
    irc_channels = forms.CharField(label="IRC Channels", required=False)
    shirt_size = forms.ChoiceField(shirt_objects)
    #role = forms.ChoiceField(vf_objects)
    requested_role = forms.ChoiceField(vf_objects)
    comments = forms.CharField(widget=forms.Textarea,min_length=1,max_length=1000,required=False,help_text="Please let us know about any special requests or circumstances.")

    def clean(self):
        if self.cleaned_data.get('password') and self.cleaned_data.get('confirm_password') and self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError(u'Please make sure your passwords match.')
        return self.cleaned_data
    
class SpeakerForm(forms.Form):
    cat_objects = list()
    audience_objects = list()
    shirt_objects = list()
    for cat in Category.objects.all():
        cat_objects.append((cat.pk,cat.name))
        
    for audience in AudienceType.objects.all():
        audience_objects.append((audience.pk,audience.name))
        
    for ss in ShirtSize.objects.all():
        shirt_objects.append((ss.pk,ss.name))
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput,min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput,min_length=6)
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    job_title = forms.CharField(required=False)
    irc_nick = forms.CharField(label="IRC Nickname", required=False)
    irc_server = forms.CharField(label="IRC Server", required=False)
    irc_channels = forms.CharField(label="IRC Channels", required=False)
    bio = forms.CharField(label="Short Bio",required=False,widget=forms.Textarea(attrs={'class':'autoexpandbox'}))
    shirt_size = forms.ChoiceField(shirt_objects)
    category = forms.ChoiceField(cat_objects)
    audience = forms.ChoiceField(audience_objects)
    title = forms.CharField()
    short_abstract = forms.CharField(widget=forms.Textarea(attrs={'class':'autoexpandbox'}),min_length=1,max_length=500,help_text="A short abstract less than 500 characters")
    photo = forms.FileField(required=False)
    
  #  long_abstract = forms.CharField(widget=forms.Textarea,min_length=1,required=False,max_length=3000)
    def clean(self):
        if self.cleaned_data.get('password') and self.cleaned_data.get('confirm_password') and self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError(u'Please make sure your passwords match.')
        return self.cleaned_data

class ContactUsForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'autoexpandbox'}))
    captcha_text = forms.CharField()
    captcha_uid = forms.CharField(widget=forms.HiddenInput())
