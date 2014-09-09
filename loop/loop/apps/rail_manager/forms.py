from django import forms


class CloneRailForm(forms.Form):
    title = forms.CharField()
    url = forms.CharField()
