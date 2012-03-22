# coding=utf-8

from django import forms
from drivertab.iodata.models import Trip

class LoadUnloadForm(forms.Form):
    customId = forms.IntegerField()
    pin = forms.CharField(max_length=25, widget=forms.PasswordInput)

    