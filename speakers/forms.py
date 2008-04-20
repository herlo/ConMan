from speakers.models import *
from django import newforms as forms
from django.newforms import ValidationError

class PresentationForm(forms.ModelForm):
    cat = forms.ModelChoiceField(Category.objects.all(),label=u'Category')
    audiences = forms.ModelMultipleChoiceField(AudienceType.objects.all())
    title = forms.CharField()
    short_abstract = forms.CharField(widget=forms.Textarea,
                                     min_length=1,
                                     max_length=5000,
                                     help_text="A short abstract less than 5000 characters")

    class Meta:
        model = Presentation
        fields = ('cat', 'audiences', 'title', 'short_abstract')

#    slides = forms.FileField(required=False)
#    long_abstract = forms.CharField(widget=forms.Textarea,min_length=1,required=False,max_length=3000)

    def clean(self):
        if self.cleaned_data.get('password') and self.cleaned_data.get('confirm_password') and self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError(u'Please make sure your passwords match.')
        return self.cleaned_data
