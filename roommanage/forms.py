import imp
from socket import fromshare
from django import forms

class RoutineForm(forms.Form):
    routine = forms.FileField(label="Upload Routine")