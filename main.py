import asyncio
import crawl
import sys

MAX_CONCURRENCY=5

async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    else:
        url = sys.argv[1]
        print(f"starting crawl of: {url}")
        site_data = await crawl.crawl_site_async(url, MAX_CONCURRENCY)
        for page_data in site_data.values():
            print(page_data)

if __name__ == "__main__":
    asyncio.run(main())
