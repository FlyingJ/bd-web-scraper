import unittest

import crawl

normalize_url_test_cases = [
	("https://www.boot.dev/blog/path", "www.boot.dev/blog/path"),
	("https://www.boot.dev/blog/path/", "www.boot.dev/blog/path"),
	("http://www.boot.dev/blog/path", "www.boot.dev/blog/path"),
	("http://www.boot.dev/blog/path/", "www.boot.dev/blog/path"),
	("ftp://www.boot.dev/blog/path//", "www.boot.dev/blog/path"),
	("https://example.com/search?stuff+things", "example.com/search"),
]

get_heading_from_html_test_cases = [
	("""<html><body><h1>Welcome to Boot.dev</h1><main><p>Learn to code by building real projects.</p><p>This is the second paragraph.</p></main></body></html>""", "Welcome to Boot.dev"),
	("""<html><body><h1>Test Title</h1></body></html>""", "Test Title"),
	("""<html><body><p>Some text</p><h2>Test Title</h2></body></html>""", "Test Title"),
	("""<html><body></body></html>""", ""),
	("""<html><body><p>text</p></body></html>""", ""),
]

get_first_paragraph_from_html_test_cases = [
	("""<html><body><p>A</p></body></html>""", "A"),
	("""<html><body><p>A</p><main><p>B</p></main></body></html>""", "B"),
	("""<html><body><p>Outside paragraph.</p><main><p>Main paragraph.</p></main></body></html>""", "Main paragraph."),
	("""<html><body></body></html>""", ""),
]

get_urls_from_html_test_cases = [
	(("""<html><body></body></html>""", "https://www.example.com/"), []),
	(("""<html><body></body></html>""", ""), []),
	(("""""", "https://www.example.com/"), []),
	(("""""", ""), []),
	(("""<html><body><a href="https://crawler-test.com">Go to Boot.dev</a><img src="/logo.png" alt="Boot.dev Logo" /></body></html>""", "https://example.com/"), ["https://crawler-test.com", "https://example.com/logo.png"]),
]

get_images_from_html_test_cases = [
	(("""<html><body></body></html>""", "https://www.example.com/"), []),
	(("""<html><body></body></html>""", ""), []),
	(("""""", "https://www.example.com/"), []),
	(("""""", ""), []),
	(("""<html><body><a href="https://crawler-test.com">Go to Boot.dev</a><img src="/logo.png" alt="Boot.dev Logo" /></body></html>""", "https://example.com/"), ["https://example.com/logo.png"]),
]

class TestCrawl(unittest.TestCase):
	def test_normalize_url(self):
		for text, expectation in normalize_url_test_cases: 
			result = crawl.normalize_url(text)
			self.assertEqual(result, expectation)

	def test_get_heading_from_html(self):
		for html, expectation in get_heading_from_html_test_cases:
			result = crawl.get_heading_from_html(html)
			self.assertEqual(result, expectation)

	def test_get_first_paragraph_from_html(self):
		for html, expectation in get_first_paragraph_from_html_test_cases:
			result = crawl.get_first_paragraph_from_html(html)
			self.assertEqual(result, expectation)

	def test_get_urls_from_html(self):
		for ((html, base_url), expectation) in get_urls_from_html_test_cases:
			result = crawl.get_urls_from_html(html, base_url)
			self.assertEqual(result, expectation)

	def test_get_images_from_html(self):
		for ((html, base_url), expectation) in get_images_from_html_test_cases:
			result = crawl.get_images_from_html(html, base_url)
			self.assertEqual(result, expectation)

if __name__ == "__main__":
	unittest.main()