from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('coocr_upload', views.coocr_upload, name='coocr_upload'),
]
