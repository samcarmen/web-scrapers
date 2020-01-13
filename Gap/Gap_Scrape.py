from bs4 import BeautifulSoup
from lxml import html
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def make_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    return soup


def get_name(soup):
    try:
        print(soup.prettify())
        name = soup.find(class_="product-title__text").text
        print(name)
        return name
    except (AttributeError, IndexError, TypeError):
        print("None")
        return None


def scrape(url_list):
    for url in url_list:
        soup = make_soup(url)
        NAME = get_name(soup)


if __name__ == '__main__':
    url_list = ["https://www.gap.com/browse/product.do?pid=473796002&rrec=true&mlink=5001,1,HP_gaphome3_rr_1&clink=1#pdp-page-content"]
    scrape(url_list)