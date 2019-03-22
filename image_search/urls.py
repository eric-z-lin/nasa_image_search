# /image_search/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),			# path for index view
    path('refined-search/', views.refined_search, name='refined_search'),	# path for refined_search page
    path('image-page/', views.image_page, name='image_page'),	# path for image metadata page
]
