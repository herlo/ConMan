from speakers.models import *
from django import newforms as forms
from django.newforms import ValidationError

class SpeakerForm(forms.Form):
    cat_objects = list()
    audience_objects = list()
#    shirt_objects = list()

#    for ss in ShirtSize.objects.all():
#        shirt_objects.append((ss.pk,ss.name))

    for cat in Category.objects.all():
        cat_objects.append((cat.pk,cat.name))
        
    for audience in AudienceType.objects.all():
        audience_objects.append((audience.pk,audience.name))
        
#    first_name = forms.CharField()
#    last_name = forms.CharField()
#    email = forms.EmailField()
#    username = forms.CharField()
#    password = forms.CharField(widget=forms.PasswordInput,min_length=6)
#    confirm_password = forms.CharField(widget=forms.PasswordInput,min_length=6)
#    job_title = forms.CharField(required=False)
#    bio = forms.CharField(label="Short Bio",required=False,widget=forms.Textarea(attrs={'class':'autoexpandbox'}))
    category = forms.ChoiceField(cat_objects)
    audience = forms.MultipleChoiceField(audience_objects)
    title = forms.CharField()
    short_abstract = forms.CharField(widget=forms.Textarea,min_length=1,max_length=5000,help_text="A short abstract less than 500 words")

#    shirt_size = forms.ChoiceField(shirt_objects)
    
#    irc_nick = forms.CharField(label="IRC Nickname", required=False)
#    irc_server = forms.CharField(label="IRC Server", required=False)
#    irc_channels = forms.CharField(label="IRC Channels", required=False)
#    photo = forms.FileField(required=False)
    
  #  long_abstract = forms.CharField(widget=forms.Textarea,min_length=1,required=False,max_length=3000)
#    captcha_uid = forms.CharField(label='captcha_uid',required=False,widget=forms.HiddenInput())
#    captcha_text = forms.CharField(label='Calculate the total above to prove you are human',required=True)

    def clean(self):
        if self.cleaned_data.get('password') and self.cleaned_data.get('confirm_password') and self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError(u'Please make sure your passwords match.')
        return self.cleaned_data
