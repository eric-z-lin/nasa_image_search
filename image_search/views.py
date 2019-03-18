from django.shortcuts import render
import requests		# for API calls

# Create your views here.

def index(request):
	# Dictionary to pass params to API
	payload = {
		# Search query
		'q': 'apollo 11',
		# Refinement by filters
		'media_type': 'image',
		'description': 'moon landing',
		'location': 'kennedy space center',
		'year_start': '1999',
		'year_end': '2009',
	}

	# url call to NASA API 
	url = 'https://images-api.nasa.gov/search'

	r = requests.get(url, params= payload)	# requests call
	print(r.url)
	print(r.text)

	return render(request, 'image_search/search.html')	# render search html