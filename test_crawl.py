import unittest

from crawl import normalize_url

normalize_url_test_cases = [
	("https://www.boot.dev/blog/path", "www.boot.dev/blog/path"),
	("https://www.boot.dev/blog/path/", "www.boot.dev/blog/path"),
	("http://www.boot.dev/blog/path", "www.boot.dev/blog/path"),
	("http://www.boot.dev/blog/path/", "www.boot.dev/blog/path"),
	("ftp://www.boot.dev/blog/path//", "www.boot.dev/blog/path"),
	("sftp://www.boot.dev//blog/path", "www.boot.dev/blog/path"),
	("https://example.com/search?stuff+things", "NNNN"),
]

class TestCrawl(unittest.TestCase):
	def test_normalize_url(self):
		for text, expectation in normalize_url_test_cases: 
			result = normalize_url(text)
			self.assertEqual(result, expectation)

if __name__ == "__main__":
	unittest.main()