from django import forms
from django.core.files.storage import default_storage
import os

class TeacherDataForm(forms.Form):
    inputFile = forms.FileField()
    outputFile = forms.FileField()

    def save(self):
        upload_inputFile = self.cleaned_data['inputFile']
        upload_outputFile = self.cleaned_data['outputFile']
        inputFile_name = default_storage.save(os.path.join('inputs', upload_inputFile.name), upload_inputFile)
        outputFile_name = default_storage.save(os.path.join('outputs', upload_outputFile.name), upload_outputFile)
        return default_storage.url(inputFile_name), default_storage.url(outputFile_name)

class UploadDataForm(forms.Form):
    epoch = forms.IntegerField(max_value=10000, min_value=1)
    inputFilePath = forms.CharField()
    outputFilePath = forms.CharField()

class AIPredictForm(forms.Form):
    testdata = forms.FileField()
    resultdata = forms.FileField()
    json = forms.CharField(label='json')
    weight = forms.CharField(label='weight')
         
