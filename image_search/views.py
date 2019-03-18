from django.shortcuts import render
import requests		# for API calls
from .models import Image, Search

# Create your views here.

def index(request):
	# Dictionary to pass params to API
	payload = {
		# Search query
		'q': 'apollo 11',
		# Refinement by filters
		'media_type': 'image',
		'description': 'eight apollo Astronauts',
		'location': 'kennedy space center',
		'year_start': '2009',
		'year_end': '2009',
	}

	past_searches = list(Search.objects.values_list('search_query', flat = True))	# get past search results

	url = 'https://images-api.nasa.gov/search'	# url call to NASA API 

	r = requests.get(url, params= payload).json()	# requests to get json

	# r is a dictionary that has 'collection': 'items', 'metadata', 'version,' and 'href'
	num_hits = r['collection']['metadata']['total_hits']	# number of items returned

	# Example dictionary in items_list
	# {
	# 	"href":"https://images-assets.nasa.gov/image/KSC-99pp0855/collection.json",
	# 	"data":[{
	# 			"description":"KENNEDY SPACE CENTER, FLA. -- Former Apollo 11 astronaut...",
	# 			"location":"Kennedy Space Center, FL",
	# 			"title":"KSC-99pp0855",
	# 			"nasa_id":"KSC-99pp0855",
	# 			"media_type":"image",
	# 			"date_created":"1999-07-16T00:00:00Z",
	# 			"center":"KSC"
	# 	}],
	# 	"links":[{
	# 		"href":"https://images-assets.nasa.gov/image/KSC-99pp0855/KSC-99pp0855~thumb.jpg",
	# 		"render":"image",
	# 		"rel":"preview"
	# 	}]
	# }	

	# Simplify the list of metadata
	metadata_list = []	# list of dictionaries for metadata
	for d in r['collection']['items']:	# items is a list of dictionaries
		# Select relevant metadata from item dictionary
		image_metadata = {
			'title': d['data'][0]['title'],
			'media_type': d['data'][0]['media_type'],
			'description': d['data'][0]['description'],	# long paragraph of text
			'location': d['data'][0]['location'],
			'date_created': d['data'][0]['date_created'][:10],
			'nasa_id': d['data'][0]['nasa_id'],			# nasa_id of object
			'media_link': d['links'][0]['href'],		# href link to media
		}
		metadata_list.append(image_metadata)

	# Pass to template html
	context = {'metadata_list': metadata_list, 'past_searches': past_searches}

	return render(request, 'image_search/search.html', context)	# render search html