# /image_search/forms.py

from django.forms import ModelForm, TextInput
from .models import Image, Search

# Form for favorite images
class ImageForm(ModelForm):
	class Meta:
		model = Image
		fields = ['nasa_id']

# Form for search functionality
class SearchForm(ModelForm):
	class Meta:
		model = Search
		fields = ['search_query']
		widgets = {'search_query': TextInput(attrs = {
			'class': 'input',
			'placeholder': 'Search for...'
		})}		# widget for text input
