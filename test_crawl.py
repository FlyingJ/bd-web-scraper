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

class TestCrawl(unittest.TestCase):
	def test_normalize_url(self):
		for text, expectation in normalize_url_test_cases: 
			result = crawl.normalize_url(text)
			self.assertEqual(result, expectation)

	def test_get_heading_from_html_basic(self):
	    input_body = '<html><body><h1>Test Title</h1></body></html>'
	    actual = crawl.get_heading_from_html(input_body)
	    expected = "Test Title"
	    self.assertEqual(actual, expected)

	def test_get_first_paragraph_from_html_main_priority(self):
	    input_body = '''<html><body>
	        <p>Outside paragraph.</p>
	        <main>
	            <p>Main paragraph.</p>
	        </main>
	    </body></html>'''
	    actual = crawl.get_first_paragraph_from_html(input_body)
	    expected = "Main paragraph."
	    self.assertEqual(actual, expected)

if __name__ == "__main__":
	unittest.main()