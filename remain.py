import crawl
import sys

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    else:
        url = sys.argv[1]
        print(f"starting crawl of: {url}")
        pages = crawl.crawl_page(url)
        for page in pages.values():
            print(page)

if __name__ == "__main__":
    main()
