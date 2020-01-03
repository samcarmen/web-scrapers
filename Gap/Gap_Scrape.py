from lxml import html
import requests
from bs4 import BeautifulSoup


def get_mainLinks(homepage):
    print("Into function")
    pageLinks = []
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

    try:
        doc = html.fromstring(page.content)
        print(doc)
        XPATH_LINK = '//*[@id="app"]/div[2]/div/div[2]/div/div/a'

        RAW_LINKS = doc.xpath(XPATH_LINK)

        LINKS = ' '.join(RAW_LINKS).strip() if RAW_LINKS else None

        for url in LINKS.split():
            print(url)
            link = "https://www.gap.com" + url
            pageLinks.append(link)

    except Exception as e:
        print(e)

    return pageLinks


if __name__ == "__main__":
    print("Starting...")
    main_links = get_mainLinks(homepage="https://www.gap.com/")