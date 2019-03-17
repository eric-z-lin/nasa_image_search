# /image_search/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),			# path for index view
]
