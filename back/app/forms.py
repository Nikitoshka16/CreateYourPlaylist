from django import forms

class DataForm(forms.Form):
    song = forms.CharField(max_length=100)
    str1 = forms.CharField(max_length=100)
    str2 = forms.CharField(max_length=1)