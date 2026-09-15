import asyncio
import crawl
import sys

from pprint import pprint

async def main():
    if not len(sys.argv) == 4:
        print("Usage:\n\tuv main.py URL MAX_CON MAX_PAGES\n")
        sys.exit(1)
    else:
        url = str(sys.argv[1])
        max_concurrency = int(sys.argv[2])
        max_pages = int(sys.argv[3])
        print(f"starting crawl of: {url}")
        print(f" - {max_concurrency} tasks")
        print(f" - {max_pages} pages")
        site_data = await crawl.crawl_site_async(url, max_concurrency, max_pages)
        for page_data in site_data.values():
            pprint(page_data)

if __name__ == "__main__":
    asyncio.run(main(), debug=True)
