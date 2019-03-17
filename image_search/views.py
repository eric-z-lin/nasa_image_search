from django.shortcuts import render

# Create your views here.

def index(request):
	return render(request, 'image_search/test.html')	# render search html