from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, urlparse

def normalize_url(url):
	url_obj = urlparse(url)
	# print(url_obj)
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

def get_images_from_html(html, base_url):
	result = []
	soup = BeautifulSoup(html, 'html.parser')
	for image in soup.find_all('img'):
		raw_image_src = image['src']
		if raw_image_src.startswith('http'):
			image_path = raw_image_src
		else:
			image_path = urljoin(base_url, raw_image_src)
		# print(f'{image} -> {image_path}')
		result.append(image_path)
	return result

def get_urls_from_html(html, base_url):
	result = []
	soup = BeautifulSoup(html, 'html.parser')
	for link in soup.find_all('a'):
		# print(f'{link} -> {link['href']}')
		result.append(link['href'])
	return result + get_images_from_html(html, base_url)