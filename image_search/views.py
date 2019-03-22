from django.shortcuts import render
import requests		# for API calls
from .models import Image, Search
from .forms import ImageForm, SearchForm

# Create your views here.

def index(request):				# Search
	if request.method == 'GET':		# e.g. type in main page
		form = SearchForm()
		past_searches = list(Search.objects.values_list('search_query', flat = True))[-10:]	# get past search results
		# Remove repeats
		for i in past_searches:
			while past_searches.count(i) > 1:
				past_searches.remove(i)
		past_searches = past_searches[-5:]	# ensure it's last 5 searches
		num_hits = 0
		context = {'metadata_list': [], 'past_searches': past_searches, 'form': form, 'num_hits': num_hits}
		return render(request, 'image_search/search.html', context)	# render search html

	elif request.method == 'POST':		# if user searched
		form = SearchForm(request.POST)		# save user form input
		q = form['search_query'].value()	# input string
		if form.is_valid():
			form.save()
		else:			# past search
			q = request.POST.get('past_submit', False)
			if q == False:
				return render(request, 'image_search/search.html')

		# Dictionary to pass params to API
		payload = {
			# Search query
			'q': q,
			'media_type': 'image',		# only images, no audio
			# Refinement by filters

			# 'description': 'eight apollo Astronauts',
			# 'location': 'kennedy space center',
			# 'year_start': '2009',
			# 'year_end': '2009',
		}

		past_searches = list(Search.objects.values_list('search_query', flat = True))[-10:]	# get past search results
		# Remove repeats
		for i in past_searches:
			while past_searches.count(i) > 1:
				past_searches.remove(i)
		past_searches = past_searches[-5:]		# ensure last 5 searches

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

		# Pass to template html
		context = {
			'metadata_list': metadata_list, 
			'past_searches': past_searches, 
			'form': form, 
			'num_hits' : num_hits,
			'q': q
		}

		return render(request, 'image_search/search.html', context)	# render search.html

def refined_search(request):		# Refined search
	if request.method == 'GET':
		form = SearchForm()
		past_searches = list(Search.objects.values_list('search_query', flat = True))[-10:]	# get past search results
		# Remove repeats
		for i in past_searches:
			while past_searches.count(i) > 1:
				past_searches.remove(i)
		past_searches = past_searches[-5:]	# ensure it's last 5 searches
		context = {'metadata_list': [], 'past_searches': past_searches, 'form': form}
		return render(request, 'image_search/refined_search.html', context)	# render search html

	elif request.method == 'POST':
		print(request.POST)
		form = SearchForm(request.POST)		# save user form input
		q = form['search_query'].value()	# input string
		if form.is_valid():
			form.save()
		else:			# past search
			q = request.POST.get('past_submit', False)
			if q == False:
				return render(request, 'image_search/search.html')

		# Dictionary to pass params to API
		payload = {
			# Search query
			'q': q,
			'media_type': 'image',		# only images, no audio
		}
		# Refinement by filters
		description = request.POST.get('description', '')
		location = request.POST.get('location', '')
		year_start = request.POST.get('year_start', '')
		year_end = request.POST.get('year_end', '')
		if description != '':
			payload['description'] = description
		if location != '':
			payload['location'] = location
		if year_start != '':
			payload['year_start'] = year_start
		if year_end != '':
			if int(year_end) < int(year_start):
				return render(request, 'image_search/search_error.html')
			else:
				payload['year_end'] = year_end

		past_searches = list(Search.objects.values_list('search_query', flat = True))[-10:]	# get past search results
		# Remove repeats
		for i in past_searches:
			while past_searches.count(i) > 1:
				past_searches.remove(i)
		past_searches = past_searches[-5:]		# ensure last 5 searches

		url = 'https://images-api.nasa.gov/search'	# url call to NASA API 

		r = requests.get(url, params= payload).json()	# requests to get json

		# r is a dictionary that has 'collection': 'items', 'metadata', 'version,' and 'href'
		num_hits = r['collection']['metadata']['total_hits']	# number of items returned
		num_hits = format(num_hits, ',')	# commas for thousands separators

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

		# Pass to template html
		context = {
			'metadata_list': metadata_list, 
			'past_searches': past_searches, 
			'form': form, 
			'num_hits' : num_hits,
			'q': q
		}

		return render(request, 'image_search/search.html', context)	# render search.html

def image_page(request):		# View image metadata
	if request.method == 'GET':
		nasa_id = request.GET.get('id', '')
		if nasa_id == '':
			# REDIRECT TO GENERIC PAGE
			return render(request, 'image_search/search.html')
		else:
			payload = {
				# Search nasa_id
				'nasa_id': nasa_id,
			}
			url = 'https://images-api.nasa.gov/search'	# url call to NASA API 
			r = requests.get(url, params= payload).json()	# requests to get json
			image_metadata = {}
			for d in r['collection']['items']:	# items is a list of dictionaries
				# Select relevant metadata from item dictionary
				if 'title' in d['data'][0]:
					image_metadata['title'] = d['data'][0]['title']
				if 'description' in d['data'][0]:
					image_metadata['description'] = d['data'][0]['description']	# long paragraph of text
				if 'location' in d['data'][0]:	
					image_metadata['location'] = d['data'][0]['location']
				if 'date_created' in d['data'][0]:
					image_metadata['date_created'] = d['data'][0]['date_created'][:10]
				if 'nasa_id' in d['data'][0]:
					image_metadata['nasa_id'] = d['data'][0]['nasa_id']			# nasa_id of object
				if 'href' in d['links'][0]:
					image_metadata['media_link'] = d['links'][0]['href']		# href link to media
			# Pass to template html
			context = {
				'image': image_metadata, 
			}
			return render(request, 'image_search/image_page.html', context)		# render image_page.html

def search_error(request):		# Error while searching
	return render(request, 'image_search/search_error.html')

def intro(request):		# Intro page
	if request.method == 'GET':	 # Display intro page
		form = SearchForm()
		past_searches = list(Search.objects.values_list('search_query', flat = True))[-10:]	# get past search results
		# Remove repeats
		for i in past_searches:
			while past_searches.count(i) > 1:
				past_searches.remove(i)
		past_searches = past_searches[-5:]	# ensure it's last 5 searches
		num_hits = 0
		context = {'metadata_list': [], 'past_searches': past_searches, 'form': form, 'num_hits': num_hits}
		return render(request, 'image_search/intro.html', context)	# render search html
	if request.method == 'POST': # Search
		form = SearchForm(request.POST)		# save user form input
		q = form['search_query'].value()	# input string
		if form.is_valid():
			form.save()
		else:			# past search
			q = request.POST.get('past_submit', False)
			if q == False:
				return render(request, 'image_search/search.html')
				
		# Dictionary to pass params to API
		payload = {
			# Search query
			'q': q,
			'media_type': 'image',		# only images, no audio
		}

		past_searches = list(Search.objects.values_list('search_query', flat = True))[-10:]	# get past search results
		# Remove repeats
		for i in past_searches:
			while past_searches.count(i) > 1:
				past_searches.remove(i)
		past_searches = past_searches[-5:]		# ensure last 5 searches

		url = 'https://images-api.nasa.gov/search'	# url call to NASA API 

		r = requests.get(url, params= payload).json()	# requests to get json

		# r is a dictionary that has 'collection': 'items', 'metadata', 'version,' and 'href'
		num_hits = r['collection']['metadata']['total_hits']	# number of items returned
		num_hits = format(num_hits, ',')	# commas for thousands separators	

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

		# Pass to template html
		context = {
			'metadata_list': metadata_list, 
			'past_searches': past_searches, 
			'form': form, 
			'num_hits' : num_hits,
			'q': q
		}

		return render(request, 'image_search/search.html', context)	# render search.html
