from django.db import models

# Create your models here.

class Image(models.Model):		# to store favorite images
	nasa_id = models.CharField(max_length=32)	# Nasa ID allows us to easily 

	def __str__(self):
		return self.nasa_id

class Search(models.Model):		# to store past searches
	search_query = models.CharField(max_length=64)	

	def __str__(self):
		return self.search_query

	class Meta:
		verbose_name_plural = 'searches'