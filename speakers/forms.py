from speakers.models import *
from django import forms
from django.forms import ValidationError

class PresentationForm(forms.ModelForm):
    cat = forms.ModelChoiceField(Category.objects.all(),label=u'Category')
    audiences = forms.ModelMultipleChoiceField(AudienceType.objects.all())
    title = forms.CharField()
    short_abstract = forms.CharField(widget=forms.Textarea,
                                     min_length=1,
                                     max_length=5000,
                                     help_text="An abstract less than 5000 characters")
    slides = forms.FileField(required=False, widget=forms.HiddenInput, label='')
#    long_abstract = forms.CharField(widget=forms.Textarea,min_length=1,required=False,max_length=3000)

    class Meta:
        model = Presentation
        fields = ('cat', 'audiences', 'title', 'short_abstract')


#    def clean(self):
#        if self.cleaned_data.get('password') and self.cleaned_data.get('confirm_password') and self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
#            raise ValidationError(u'Please make sure your passwords match.')
#        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(PresentationForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.status.name == 'Approved':
            self['cat'].field.widget.attrs.update({'disabled': True})
            self['cat'].field.required = False
            self['audiences'].field.widget.attrs.update({'disabled': True})
            self['audiences'].field.required = False
            self['title'].field.widget.attrs.update({'disabled': 'disabled'})
            self['title'].field.required = False
            self['short_abstract'].field.widget.attrs.update({'disabled': 'disabled'})
            self['short_abstract'].field.required = False
            self['slides'].field.widget = forms.FileInput()
            self['slides'].field.label = 'Slide Deck'

class PresentationSlidesForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ('slides',)

