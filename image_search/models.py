from django.db import models

# Create your models here.

class Search(models.Model):		# to store past searches
	search_query = models.CharField(max_length=64)	

	def __str__(self):
		return self.search_query

	class Meta:
		verbose_name_plural = 'searches'