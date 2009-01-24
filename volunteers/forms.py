    
from volunteers.models import *
from django import forms
from django.forms import ValidationError

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

