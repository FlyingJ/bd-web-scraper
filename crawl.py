from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse

def normalize_url(url):
	url_obj = urlparse(url)
	print(url_obj)
	return url_obj.netloc + url_obj.path.rstrip('/')

def get_heading_from_html(html):
	result = "" # default return empty string
	soup = BeautifulSoup(html, 'html.parser')
	if soup.h1:
		result = soup.h1.string
	elif soup.h2:
		result = soup.h2.string
	return result

def get_first_paragraph_from_html(html):
	result = "" # default return empty string
	soup = BeautifulSoup(html, 'html.parser')
	if soup.main and soup.main.p:
		result = soup.main.p.string
	elif soup.p:
		result = soup.p.string
	return result
