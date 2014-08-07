# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth.models import Permission, User

class UserloginForm(forms.Form):
    username = forms.CharField(label=u'ผู้ใช้', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=u'รหัสผ่าน', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
