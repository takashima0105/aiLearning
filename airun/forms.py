from django import forms
from .models import TeacherData

class TeacherDataForm(forms.ModelForm):
    class Meta:
        model = TeacherData
        fields = ('epoch', 'inputFile', 'outputFile', )
 
class AIPredictForm(forms.Form):
    testdata = forms.FileField()
    resultdata = forms.FileField()
    json = forms.CharField(label='json')
    weight = forms.CharField(label='weight')
         
