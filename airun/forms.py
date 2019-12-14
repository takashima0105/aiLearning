from django import forms

class UploadFileForm(forms.Form):
    inputfile = forms.FileField()
    outputfile = forms.FileField()