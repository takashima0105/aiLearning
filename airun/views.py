from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms.widgets import NumberInput
from django.views import generic
from .forms import TeacherDataForm, UploadDataForm
from django.urls import reverse
from .learning import Prediction
from .graghcreate import GraphCreate
import sys
from django.contrib.auth.decorators import login_required#if no athuentication, execute redirect
import os
from .forms import AIPredictForm
from .prediction import Predict

# ------------------------------------------------------------------------------------
#学習実効画面の表示 & ファイルアップロード処理
class DataUpload(generic.FormView):

    template_name = 'airun/main.html'
    test_name = 'airun/test.html'
    form_class = TeacherDataForm
    pathform_class = UploadDataForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        contexts = {'form':form}
        return render(request, self.template_name, contexts)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES or None)
        if form.is_valid():
            for file in form.files:
                root, ext = os.path.splitext(form.files[file].name)
                if ext != '.csv':
                    message = 'csvファイルをアップロードしてください。'
                    form = self.form_class(initial=self.initial)
                    contexts = {'form':form, 'message':message}
                    return render(request, self.template_name, contexts)

            obj = form.save()
            
            gc = GraphCreate(obj[0], obj[1])
            indexs, scripts, datanum = gc.Create()
            pathform = self.pathform_class(initial={
                'epoch':100,
                'batchSize':datanum,
                'hiddenLayer':3,
                'node':100,
                'testSize':30,
                'inputFilePath':obj[0],
                'outputFilePath':obj[1]
            })

            pathform.fields['batchSize'].validators.append(MaxValueValidator(datanum))
            pathform.fields['batchSize'].validators.append(MinValueValidator(1))
            pathform.fields['batchSize'].widget = NumberInput(attrs={'max':datanum, 'min':1})

            contexts = {'form':pathform, 'obj':obj , 'indexs':indexs, 'scripts':scripts}
            return render(request, self.template_name, contexts)
            # predict = Prediction(obj.inputFile.path, obj.outputFile.path, obj.epoch)
            # aimodel = predict.main()
            # json = os.path.abspath(aimodel[0])
            # weight = os.path.abspath(aimodel[1])
            # formset = next_form(initial=self.initial)
            # formset.initial = {'json': json, 'weight': weight}
            # contexts = {'form':formset}
            # return render(request, self.test_name,contexts)
# ------------------------------------------------------------------------------------
#予測テスト
class TestStart(generic.FormView):
    form_data = AIPredictForm
    page = 'airun/test.html'

    def post(self, request, *args, **kwargs):
        form = self.form_data(request.POST, request.FILES or None)
        # for file in form.files:
        #         root, ext = os.path.splitext(form.files[file].name)
        #         if ext != '.csv':
        #             message = 'csvファイルをアップロードしてください。'
        #             form = self.form_data(initial=self.initial)
        #             contexts = {'form':form, 'message':message}
        #             return render(request, self.template_name, contexts)
        
        obj = form
        test = Predict(obj.testdata, obj.resultdata, obj.json, obj.weight)
        result = test.run()
        contexts = {'fomm':result}

        return render(request, self.page, contexts)
    
# Create your views here.
