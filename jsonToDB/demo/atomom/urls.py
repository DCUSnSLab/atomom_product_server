from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.coocr_upload, name='home'),
    path('coocr_upload', views.coocr_upload, name='coocr_upload'),
    path('api', views.api, name='api'),
]
