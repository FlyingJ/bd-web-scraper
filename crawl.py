import requests

from bs4 import BeautifulSoup, Tag
from typing import TypedDict
from urllib.parse import urljoin, urlparse

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def crawl_page(
	base_url: str,
	current_url: str = None,
	site_data: dict[str, PageData] = None
	) ->  dict[str, PageData]:
	if not site_data:
		site_data = {}
	
	if not current_url.startswith(base_url):
		print(f"SKIP: {current_url} outside {base_url}")
		return site_data

	norm_current_url = normalize_url(current_url)
	if norm_current_url not in site_data:
		print(f"CACHE MISS: {norm_current_url}")
		page_data = extract_page_data(get_html(current_url), current_url)
		site_data[norm_current_url] = page_data
		for link in page_data["outgoing_links"]:
			print(f"FOUND ANOTHER PAGE: {link}")
			site_data = crawl_page(base_url, link, site_data)
	else:
		print(f"CACHE HIT: {norm_current_url}")
	return site_data

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

def get_first_paragraph_from_html(html: str) -> str:
	result = "" # default return empty string
	soup = BeautifulSoup(html, 'html.parser')
	if soup.main and soup.main.p:
		result = soup.main.p.string
	elif soup.p:
		result = soup.p.string
	return result

def get_heading_from_html(html: str) -> str:
	result = "" # default return empty string
	soup = BeautifulSoup(html, 'html.parser')
	if soup.h1:
		result = soup.h1.string
	elif soup.h2:
		result = soup.h2.string
	return result

def get_images_from_html(html: str, base_url: str) -> list[str]:
	return [urljoin(base_url, image["src"]) for image in BeautifulSoup(html, 'html.parser').find_all('img')]

def get_urls_from_html(html: str, base_url: str) -> list[str]:
	return [urljoin(base_url, link["href"]) for link in BeautifulSoup(html, 'html.parser').find_all('a')]

def normalize_url(url: str) -> str:
	url_obj = urlparse(url)
	return url_obj.netloc + url_obj.path.rstrip('/')

def get_html(url: str) -> str:
	headers = {
		"User-Agent": "BootCrawler/1.0",
	}
	result = requests.get(url, headers=headers)
	if result.status_code >= 400:
		result.raise_on_status()
	if not result.headers["content-type"].startswith("text/html"):
		raise Exception(f'response has incorrect Content-Type: {result.headers["content-type"]}')
	print(f"Fetched page: {url}")
	return result.text