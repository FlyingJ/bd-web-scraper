import aiohttp
import asyncio
import requests

from bs4 import BeautifulSoup, Tag
from typing import TypedDict
from urllib.parse import urljoin, urlparse, urlsplit

class AsyncCrawler():
	def __init__(self, url, max_concurrency=1):
		self.base_url = url
		self.base_domain = urlsplit(self.base_url).netloc

		self.site_data = {}
		self.lock = asyncio.Lock()
		self.max_concurrency = max_concurrency
		self.semaphore = asyncio.Semaphore(self.max_concurrency)
		self.session = None

	async def __aenter__(self):
		self.session = aiohttp.ClientSession()
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		await self.session.close()

	async def add_page_visit(self, normalized_url):
		try:
			if self.lock is None:
				raise Exception("no lock allocated in AsyncCrawler object")
			async with self.lock:
				if normalized_url not in self.site_data:
					self.site_data[normalized_url] = {}
					return True
				else:
					return False
		except Exception as e:
			print(f"Exception caught: {e}")
			return None

	async def get_html(self, url):
		try:
			headers = {
				"User-Agent": "BootCrawler/1.0",
			}
			if self.session is None:
				return None
			async with self.session.get(url, headers=headers) as response:
				if response.status >= 400:
					raise Exception(f"HTTP error status: {response.status} {response.reason}")
				if "content-type" not in response.headers:
					raise Exception("Content-Type header missing from response")
				if "text/html" not in response.headers.get("content-type", ""):
					raise Exception(f'incorrect Content-Type: {response.headers.get("content-type", "")}')
				# print(f"Fetched page: {url}")
				return await response.text()
		except Exception as e:
			print(f"Exception caught: {e}")
			return None

	async def crawl_page(self, current_url: str = None):
		try:
			if current_url is None:
				print("ODD: current_url is None")
				return
			if not urlsplit(current_url).netloc == self.base_domain:
				print(f"SKIP: {urlsplit(current_url).netloc} not in {self.base_domain}")
				return
			normalized_url = normalize_url(current_url)
			if not await self.add_page_visit(normalized_url):
				return

			async with self.semaphore:
				html = await self.get_html(current_url)
			
			if html is None:
				return
			page_data = extract_page_data(html, current_url)

			async with self.lock:
				self.site_data[normalized_url] = page_data
			
			tasks = set()
			for url in page_data["outgoing_links"]:
				task = asyncio.create_task(self.crawl_page(url))
				tasks.add(task)
			if tasks:
				await asyncio.gather(*tasks)
		except Exception as e:
			print(f"Exception in AsyncCrawler.crawl_page(): {e}")

	async def crawl(self):
		await self.crawl_page(self.base_url)
		return self.site_data

async def crawl_site_async(url):
	async with AsyncCrawler(url) as crawler:
		return await crawler.crawl()

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
		# print(f"SKIP: {current_url} outside {base_url}")
		return site_data

	normalized_url = normalize_url(current_url)
	if normalized_url not in site_data:
		print(f"FETCH: {normalized_url}")
		site_data[normalized_url] = extract_page_data(get_html(current_url), current_url)
		for link in site_data[normalized_url]["outgoing_links"]:
			# print(f"FOUND ANOTHER PAGE: {link}")
			site_data = crawl_page(base_url, link, site_data)
	# else:
	# 	print(f"CACHE HIT: {normalized_url}")
	return site_data

def extract_page_data(html: str, page_url: str) -> PageData:
	base_domain = get_base_domain(page_url)
	if base_domain is None:
		return None
	# print(f'Page URL: {page_url}')
	# print(f'Base URL: {base_url}')
	return {
		"url": page_url,
		"heading": get_heading_from_html(html),
		"first_paragraph": get_first_paragraph_from_html(html),
		"outgoing_links": get_urls_from_html(html, base_domain),
		"image_urls": get_images_from_html(html, base_domain),
	}

def get_base_domain(url: str) -> str:
	try:
		url_obj = urlsplit(url)
		result = f"{url_obj.scheme}://{url_obj.netloc}"
	except ValueError as v:
		print(f"ValueError encountered during get_base_domain. Likely bad URL: {v}")
		result = None
	except Exception as e:
		print("Generic exception: {e}")
		result = None
	finally:
		return result

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
	url_obj = urlsplit(url)
	return url_obj.netloc + url_obj.path.rstrip('/')

def get_html(url: str) -> str:
	try:
		headers = {
			"User-Agent": "BootCrawler/1.0",
		}
		response = requests.get(url, headers=headers)
		if response.status_code >= 400:
			raise Exception(f"HTTP error status: {response.status} {response.reason}")
		if "content-type" not in response.headers:
			raise Exception("Content-Type header missing from response")
		if "text/html" not in response.headers.get("content-type", ""):
			raise Exception(f'incorrect Content-Type: {response.headers.get("content-type", "")}')
		# print(f"Fetched page: {url}")
		return response.text
	except Exception as e:
		print(f"Exception caught: {e}")
		return None
