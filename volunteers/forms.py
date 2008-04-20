#from common.models import ShirtSize
#from volunteers.models import *
#from django import newforms as forms
#from django.newforms import ValidationError

#class VolunteerForm(forms.Form):
    #vf_objects = list()
    #shirt_objects = list()
    #for vf in VolunteerRole.objects.all():
        #vf_objects.append((vf.pk,vf.name))
    
    #for ss in ShirtSize.objects.all():
        #shirt_objects.append((ss.pk,ss.name))

    #first_name = forms.CharField()
    #last_name = forms.CharField()
    #email = forms.EmailField()
    #job_title = forms.CharField(required=False)
    #irc_nick = forms.CharField(label="IRC Nickname", required=False)
    #irc_server = forms.CharField(label="IRC Server", required=False)
    #irc_channels = forms.CharField(label="IRC Channels", required=False)
    #shirt_size = forms.ChoiceField(shirt_objects)
    ##role = forms.ChoiceField(vf_objects)
    #requested_role = forms.ChoiceField(vf_objects)
    #comments = forms.CharField(widget=forms.Textarea,min_length=1,max_length=1000,required=False,help_text="Please let us know about any special requests or circumstances.")

    #def clean(self):
        #if self.cleaned_data.get('password') and self.cleaned_data.get('confirm_password') and self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            #raise ValidationError(u'Please make sure your passwords match.')
        #return self.cleaned_data
    
    
from volunteers.models import *
from django import newforms as forms
from django.newforms import ValidationError

class VolunteerForm(forms.ModelForm):
    cat = forms.ModelChoiceField(Category.objects.all(),label=u'Category')
    audiences = forms.ModelMultipleChoiceField(AudienceType.objects.all())
    title = forms.CharField()
    short_abstract = forms.CharField(widget=forms.Textarea,
                                     min_length=1,
                                     max_length=5000,
                                     help_text="A short abstract less than 5000 characters")

    #role = forms.ModelChoiceField(VolunteerRole.objects.all(),label=u'Role')
    #models.ForeignKey(VolunteerRole,related_name='role',blank=True, null=True)
    request = forms.ModelChoiceField(VolunteerRole.objects.all(),label=u'Requested Role')
    #models.ForeignKey(VolunteerRole, related_name='request')
    comments = forms.CharField(widget=forms.Textarea,
                                     min_length=1,
                                     max_length=5000,
                                     help_text="A any comments or special requests, less than 5000 characters")

    #models.TextField()
    #volunteer = models.ForeignKey(UserProfile)
    class Meta:
        model = Volunteer
        fields = ('request', 'comments')

#    slides = forms.FileField(required=False)
#    long_abstract = forms.CharField(widget=forms.Textarea,min_length=1,required=False,max_length=3000)

    def clean(self):
        if self.cleaned_data.get('password') and self.cleaned_data.get('confirm_password') and self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError(u'Please make sure your passwords match.')
        return self.cleaned_data

