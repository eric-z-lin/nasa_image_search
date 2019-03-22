# /image_search/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.intro, name='intro'),			# path for intro view
    path('index/', views.index, name='index'),		# path for index view
    path('refined-search/', views.refined_search, name='refined_search'),	# path for refined_search view
    path('image-page/', views.image_page, name='image_page'),	# path for image metadata view
    path('search-error/', views.search_error, name='search_error'),	# path for search error view
]
