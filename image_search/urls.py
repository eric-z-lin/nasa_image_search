# /image_search/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),			# path for index view
    path('./image-page', views.image_page)	# path for image metadata page
]
