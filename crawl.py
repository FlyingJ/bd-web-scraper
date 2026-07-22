from bs4 import BeautifulSoup, Tag
from typing import TypedDict
from urllib.parse import urljoin, urlparse

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def extract_page_data(html: str, page_url: str) -> PageData:
	obj = urlparse(page_url)
	base_url = f'{obj.scheme}://{obj.netloc}'
	# print(f'Page URL: {page_url}')
	# print(f'Base URL: {base_url}')
	return {
		"url": page_url,
		"heading": get_heading_from_html(html),
		"first_paragraph": get_first_paragraph_from_html(html),
		"outgoing_links": get_urls_from_html(html, base_url),
		"image_urls": get_images_from_html(html, base_url),
	}

def get_first_paragraph_from_html(html):
	result = "" # default return empty string
	soup = BeautifulSoup(html, 'html.parser')
	if soup.main and soup.main.p:
		result = soup.main.p.string
	elif soup.p:
		result = soup.p.string
	return result

def get_heading_from_html(html):
	result = "" # default return empty string
	soup = BeautifulSoup(html, 'html.parser')
	if soup.h1:
		result = soup.h1.string
	elif soup.h2:
		result = soup.h2.string
	return result

def get_images_from_html(html, base_url):
	return [urljoin(base_url, image["src"]) for image in BeautifulSoup(html, 'html.parser').find_all('img')]

def get_urls_from_html(html, base_url):
	return [urljoin(base_url, link["href"]) for link in BeautifulSoup(html, 'html.parser').find_all('a')]

def normalize_url(url):
	url_obj = urlparse(url)
	# print(url_obj)
	return url_obj.netloc + url_obj.path.rstrip('/')
