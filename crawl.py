from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse

def normalize_url(url):
	url_obj = urlparse(url)
	print(url_obj)
	return url_obj.netloc + url_obj.path.rstrip('/')

def get_heading_from_html(html):
	result = "" # default return empty string
	return result

def get_first_paragraph_from_html(html):
	return None
