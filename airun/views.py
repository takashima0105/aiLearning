from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from .forms import TeacherDataForm
from .models import TeacherData
from django.urls import reverse
from .learning import Prediction
import sys
<<<<<<< HEAD:airun2/views.py
from django.contrib.auth.decorators import login_required#if no athuentication, execute redirect

# ------------------------------------------------------------------
#学習実効画面の表示
@login_required #if no athuentication, execute redirect to /login/
def airun_display(request):
    form = UploadFileForm()
    return render(request, 'airun/airun.html', {"form": form })
# ------------------------------------------------------------------
#ファイルアップロード処理
def file_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
=======
import os

# ------------------------------------------------------------------------------------
#学習実効画面の表示 & ファイルアップロード処理
class DataUpload(generic.FormView):
    template_name = 'airun/main.html'
    form_class = TeacherDataForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        contexts = {'form':form}
        return render(request, self.template_name, contexts)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES or None)
        
>>>>>>> 5c59b7a1908100ddd8abcfb246253dce89ebc360:airun/views.py
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
            predict.main()

            contexts = {'form':form}
            return render(request, self.template_name, contexts)
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

# ------------------------------------------------------------------------------------

# Create your views here.
