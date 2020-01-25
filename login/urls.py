from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.Login, name="login"),
    path('auth/', include('social_django.urls', namespace='social')), # move to oauth athuentication
]

