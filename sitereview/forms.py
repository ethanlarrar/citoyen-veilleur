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
        fields = [
            #'creator'
            'title',
            'url',
            'remark',
            #'deleted',
            #'date',
            #'verify',
            #'site_closed',
            'hour_video',
            'minute_video',
            'second_video',
            'main_quotes',
            'antisem_france',
            'antisem_abroad',
            'antisionisme_france',
            'antisionisme_abroad',
            'video',
            'article',
            'social_network',
            'comments',
            'regular_website',
            'official_hater_website',
            'legal_proceeding',
            'only_alert',
            'bad_user',
            'extern_pseudo',
            #'voted_by',
        ]
