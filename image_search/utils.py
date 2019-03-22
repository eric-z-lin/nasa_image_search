# image_search/utils.py
# Helper functions for views.py 
import requests		# for api calls
from .models import Search 	# for past searches

def api_query(q):	# query NASA api and return data
	# Dictionary to pass params to API
	payload = {
		'q': q,		# Search query
		'media_type': 'image',		# only images, no audio
	}

	url = 'https://images-api.nasa.gov/search'	# url call to NASA API 

	r = requests.get(url, params= payload).json()	# requests to get json

	# r is a dictionary that has 'collection': 'items', 'metadata', 'version,' and 'href'
	num_hits = r['collection']['metadata']['total_hits']	# number of items returned
	num_hits = format(num_hits, ',')	# commas for thousands separators
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
			'nasa_id': d['data'][0]['nasa_id'],			# nasa_id of object
			'media_link': d['links'][0]['href'],		# href link to media
		}
		metadata_list.append(image_metadata)

	return metadata_list, num_hits

def find_past_searches():
	past_searches = list(Search.objects.values_list('search_query', flat = True))[-10:]	# get past search results
	# Remove repeats
	for i in past_searches:
		while past_searches.count(i) > 1:
			past_searches.remove(i)
	past_searches = past_searches[-5:]		# ensure last 5 searches
	return past_searches