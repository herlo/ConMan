from common.models import ShirtSize
from volunteers.models import *
from django import newforms as forms
from django.newforms import ValidationError

class VolunteerForm(forms.Form):
    vf_objects = list()
    shirt_objects = list()
    for vf in VolunteerRole.objects.all():
        vf_objects.append((vf.pk,vf.name))
    
    for ss in ShirtSize.objects.all():
        shirt_objects.append((ss.pk,ss.name))

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
