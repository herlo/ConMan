from django import forms
from django.forms import ValidationError
from volunteers.models import Volunteer, VolunteerRole


class VolunteerForm(forms.ModelForm):
    requested = forms.ModelChoiceField(VolunteerRole.objects.all(),
                                       label=u'Requested Role')
    comments = forms.CharField(widget=forms.Textarea,
                               min_length=1,
                               max_length=5000,
                               help_text="A any comments or special requests, less than 5000 characters")

    class Meta:
        model = Volunteer
        hidden_fields = ("volunteer")
        fields = ("requested", "comments")
