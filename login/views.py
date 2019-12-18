from django.shortcuts import render
from django.http import HttpResponse

def Login(request):
    return render(request, "login/login.html")
    

# Create your views here.
