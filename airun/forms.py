from django import forms
from .models import TeacherData

class TeacherDataForm(forms.ModelForm):
    class Meta:
        model = TeacherData
        fields = ('epoch', 'inputFile', 'outputFile', )
 
class AIPredictForm(forms.Form):
    fields = ('testdata', 'resultdata','json','weight')
         
