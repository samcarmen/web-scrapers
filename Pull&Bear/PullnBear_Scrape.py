from bs4 import BeautifulSoup
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def make_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    return soup


def get_name(soup):
    name = soup.find(id="titleProductCard")
    print(name)


if __name__ == '__main__':
    url = "https://www.pullandbear.com/my/woman/sale/clothing/coats-and-jackets/double-button-synthetic-wool-coat-c1030204597p501552450.html?cS=800"
    soup = make_soup(url)
    print(soup.prettify())
    get_name(soup)