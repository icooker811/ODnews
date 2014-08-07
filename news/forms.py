# -*- encoding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from news.models import NewsCategory,NewsPublish


class NewsForm(forms.Form):
    title = forms.CharField(label=u'หัวข้อ', max_length=75 , validators=[
        RegexValidator(
                regex='^[A-Z][a-zA-Z0-9]*$',
                message='Title must be start with [A-Z]. Only alpha numeric allow',
                code='invalid_title'
            ),
        ], widget=forms.TextInput(attrs={'class': 'form-control'}))
    stitle = forms.CharField(label=u'คำโปรย', max_length=150 , widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label=u'เนื้อหาข่าว', max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}))
    image = forms.ImageField(label=u'รูปภาพประกอบข่าว', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(label=u'ประเภทข่าว', queryset=NewsCategory.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    
    
    def clean_description(self):

        if (self.cleaned_data.get('stitle') not in self.cleaned_data.get('description')):
            raise ValidationError("This news teaser is not in description")
        return self.cleaned_data.get('description')



