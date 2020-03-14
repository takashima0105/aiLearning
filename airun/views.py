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
from .prediction import Predict
from .prediction import Kickoff
from .resultdata import ResultGraph


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

def chart_create(request):
    
    form_class = TeacherDataForm
    form = form_class(request.POST, request.FILES or None)
    pathform_class = UploadDataForm

    if form.is_valid():
        obj = form.save()
        gc = GraphCreate(obj[0], obj[1])
        indexs, scripts, datanum = gc.Create()
        pathform = pathform_class(initial={
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
        return render(request, 'airun/chart.html', contexts)

# ------------------------------------------------------------------------------------
#AIの作成と予測の実行
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
                    'testSize':request.POST['testSize']
                    }

        #学習のためのインスタンス作成
        predict = Prediction(contexts)

        #学習開始、モデルファイルと重みファイルを作成
        aimodel = predict.main()

        #モデルファイルのパスを取得
        json = os.path.abspath(aimodel[0])
        
        #重みファイルのパスを取得
        weight = os.path.abspath(aimodel[1])

        #予測のためのインスタンス作成
        test = Kickoff(request.POST['inputFilePath'], request.POST['outputFilePath'], json, weight)
        
        #予測実行、実際の値と予測値を２次元配列で出力
        result = test.run()

        #学習データのグラフ作成
        realgc = ResultGraph(result[0][0], result[0][1],result[1][1])
        indexs, scripts = realgc.Create()

        contexts = {'indexs':indexs, 'scripts':scripts}

        return render(request, self.template_name, contexts)
    
# Create your views here.
