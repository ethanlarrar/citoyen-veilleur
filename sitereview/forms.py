from django import forms
from .models import Website_alert

# https://docs.djangoproject.com/en/2.1/topics/forms/
# Method 1
class CreateFormOld(forms.Form):
    title = forms.CharField(max_length=200)
    url = forms.URLField(max_length=255)
    remark = forms.CharField(widget=forms.Textarea)

# https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/
# Method 2
class CreateForm(forms.ModelForm):
    class Meta:
        model = Website_alert
        fields = ['title','url','remark']
