from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from .forms import TeacherDataForm
from .models import TeacherData
from django.urls import reverse
from .learning import Prediction
import sys
from django.contrib.auth.decorators import login_required#if no athuentication, execute redirect
import os
from .forms import AIPredictForm

# ------------------------------------------------------------------------------------
#学習実効画面の表示 & ファイルアップロード処理
class DataUpload(generic.FormView):

    template_name = 'airun/main.html'
    test_name = 'airun/test.html'
    form_class = TeacherDataForm

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
            predict = Prediction(obj.inputFile.path, obj.outputFile.path, obj.epoch)
            aimodel = predict.main()
            json = str(aimodel[0])
            weight = str(aimodel[1])

            contexts = {'json':json, 'weight':weight}
            return render(request, self.test_name, contexts)
# ------------------------------------------------------------------------------------

#アップロードファイルの確認
class DataVerification(generic.DetailView):
    template_name = 'airun/verification.html'
    main_name = 'airun/main.html'
    form_class = TeacherDataForm
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES or None)
        if form.is_valid():
            obj = form.save()
            contexts = {'form':form}
            return render(request, self.template_name)
        else:
            inputtext = "Upload Failure"
            outputtext = "Upload Failure"
            contexts = {'inputtext':inputtext, 'outputtext':outputtext, 'form':form}
            return render(request, self.main_name, contexts)
# ------------------------------------------------------------------------------------
#予測テスト
class TestStart(generic.FormView):
    form = AIPredictForm

    def post(self, request, *args, **kwargs):
        if form.is_valid():
            root, ext = os.path.splitext(form.files.name)
        
    obj = form.save()
    test = predict(obj.testdata.path, obj.resultdata.path, obj.jsonfile, obj.weightfile)
    result = test.run()
    


    






# ------------------------------------------------------------------------------------

# Create your views here.
