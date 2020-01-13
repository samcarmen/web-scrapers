from bs4 import BeautifulSoup
import json
import re
import requests


def make_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    return soup


def get_name(soup):
    try:
        name = soup.find('h1', {'class':"product-name"}).text
        name = name.replace(' Details', '')
        return name
    except (AttributeError, IndexError, TypeError):
        return None


def get_price(soup):
    print(soup.find(id="popup-composition"))
    # main_price = soup.find(class_="main-price")
    # if main_price is None:
    #     original_price = soup.find(class_="line-through").text
    #     original_price = re.match(re.compile(r'\d+.\d+'), original_price)
    #     sales_price = soup.find(class_="sale discount-percentage").text
    #     sales_price = re.match(re.compile(r'\d+.\d+'), sales_price)
    #     return original_price, sales_price
    # else:
    #     price = main_price.text
    #     price = re.match(re.compile(r'\d+.\d+'), price)
    #     return price, price
    return None, None


def scrape(url_list):
    FINAL_OUTPUT = []
    for url in url_list:
        soup = make_soup(url)
        NAME = get_name(soup)
        ORI_PRICE, SALES_PRICE = get_price(soup)

        output = {
            "NAME": NAME,
            "ORIGINAL_PRICE": {
                "PRICE": ORI_PRICE,
                "CURRENCY": "RM"
            },
            "SALES_PRICE": {
                "PRICE": SALES_PRICE,
                "CURRENCY": "RM"
            }
        }

        FINAL_OUTPUT.append(output)

    pretty_output = json.dumps(FINAL_OUTPUT, indent=3)
    print(pretty_output)


if __name__ == '__main__':
    url_list = ["https://www.zara.com/my/en/masculine-coat-with-pockets-p01255233.html?v1=33523507&v2=1420674",
                "https://www.zara.com/my/en/chunky-knit-cardigan-p03859002.html?v1=40964203&v2=1445718"]
    scrape(url_list)