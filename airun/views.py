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
from .prediction import kickoff


# ------------------------------------------------------------------------------------
#学習実効画面の表示 & ファイルアップロード処理
class DataUpload(generic.FormView):

    template_name = 'airun/main.html'
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
    template_name = 'airun/test.html'
    form_class = UploadDataForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES or None)
        # form = self.pathform_class(request.POST)
        # if form.is_valid():
        #     for file in form.files:
        #         root, ext = os.path.splitext(form.files[file].name)
        #         if ext != '.csv':
        #             message = 'csvファイルをアップロードしてください。'
        #             form = self.form_class(initial=self.initial)
        #             contexts = {'form':form, 'message':message}
        #             return render(request, self.template_name, contexts)
        contexts = {'inputData':request.POST['inputFilePath'],
                    'outputData':request.POST['outputFilePath'],
                    'epoch':request.POST['epoch'],
                    'batchSize':request.POST['batchSize'],
                    'hiddenLayer':request.POST['hiddenLayer'],
                    'node':request.POST['node'],
                    'testSize':request.POST['testSize']}

        predict = Prediction(contexts)
        aimodel = predict.main()
        json = os.path.abspath(aimodel[0])
        weight = os.path.abspath(aimodel[1])
        test = Predict(request.POST['inputFilePath'], request.POST['outputFilePath'], json, weight)
        result = test.run()

        realgc = ResultGraph(result[0][0], result[0][1])
        indexs, scripts = realgc.Create()

        testgc = ResultGraph(result[1][0], result[1][1])
        testin, testsc = testgc.Create()

        contexts = { 'indexs':indexs, 'scripts':scripts, 'testin':testin, 'testsc':testsc}

        return render(request, self.template_name, contexts)
    
# Create your views here.
