from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'airun'

urlpatterns = [
    #実効画面
    path('main/', views.DataUpload.as_view(), name='DataUpload'),
    path('test/', views.TestStart.as_view(), name='TestStart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)