from django.shortcuts import render
from listing_app import models
from  .models import Search
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus

BASE_SITE_URL = 'https://kerala.craigslist.org/search/?query={}'

# Create your views here.
def home(request):
	return render(request,'index.html')

def new(request):
	search=request.POST.get('searchitem')
	models.Search.objects.create(search=search)
	site_url= BASE_SITE_URL.format(quote_plus(search))
	response=requests.get(site_url)
	data=response.text
	soup=BeautifulSoup(data,features='html.parser')
	all_posts=soup.find_all('li',{'class':'result-row'})
	all_postings=[]
	for post in all_posts:
		title=post.find(class_='result-title').text
		url=post.find('a').get('href')
		if post.find(class_='result-price'):
			price=post.find(class_='result-price').text
		else:
			price='N/A'
			
		all_postings.append((title,url,price))
	context={'search':search,
	'all_postings':all_postings,}
	return render(request,'new.html',context)
	
	
	
	
      	