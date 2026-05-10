from urllib.parse import urlparse

def normalize_url(url):
	url_obj = urlparse(url)
	print(url_obj)
	return url_obj.netloc + url_obj.path.rstrip('/')