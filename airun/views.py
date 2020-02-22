from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
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
            pathform = self.pathform_class(initial={
                'epoch':100,
                'inputFilePath':obj[0],
                'outputFilePath':obj[1]
            })
            gc = GraphCreate(obj[0], obj[1])
            indexs, scripts = gc.Create()

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
# ----------------------------------------------------------------------------------
#予測テスト
class TestStart(generic.FormView):
    page = 'airun/test.html'
    pathform_class = UploadDataForm

    def post(self, request, *args, **kwargs):
        # form = self.pathform_class(request.POST)
        # if form.is_valid():
        #     for file in form.files:
        #         root, ext = os.path.splitext(form.files[file].name)
        #         if ext != '.csv':
        #             message = 'csvファイルをアップロードしてください。'
        #             form = self.form_class(initial=self.initial)
        #             contexts = {'form':form, 'message':message}
        #             return render(request, self.template_name, contexts)

        predict = Prediction(request.POST['inputFilePath'], request.POST['outputFilePath'], request.POST['epoch'])
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

        return render(request, self.page, contexts)
    
# Create your views here.
