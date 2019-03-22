# NASA Image Search

Website for searching images using NASA's API.


Functionality:  
1. Search Function of displaying images from NASA's Image API.  
2. View image metadata for individual search results by clicking on the pictures.  
3. Advanced search with refinement by description, location, and date range (year_start and year_end).  
4. Ability to share picture on Facebook and Twitter (links in image metadata pages).
5. Seeing past searches (limited to past 5) and clicking on them to search them again.


Program Design:   
This web application uses the Django framework.  
- nasa_images directory 
	- contains the project root settings, urls
- image_search app
	- this Django app contains all the responsive pages and functionality for searching and displaying images
	- /image_search/templates/image_search contains all the html pages 
	- views.py has views functions to communicate with html pages
	- utils.py has helper functions used in views.py
	- forms.py handles the search form request
	- models.py has the search model, storing searches in database
	- urls.py handles the URLs in image_search app
	- admin.py sets up the admin (which can view the models and database)
- static directory 
	- css contains the custom css styling (used in conjunction with )
	- images contains images and icons

Admin credentials:  
Username/Email: super_user@test.com  
Password: super_user_password  