# /image_search/forms.py

from django.forms import ModelForm, TextInput
from .models import Search

# Form for search functionality
class SearchForm(ModelForm):
	class Meta:
		model = Search
		fields = ['search_query']
		widgets = {'search_query': TextInput(attrs = {
			'class': 'input',
			'placeholder': 'Search for...'
		})}		# widget for text input
