import time

from bs4 import BeautifulSoup
import json
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def make_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    return soup


def get_name(soup):
    try:
        name = soup.find(class_="ProductDetail-title").text
        return name
    except (AttributeError, IndexError, TypeError):
        return None


def get_price(soup):
    try:
        price = soup.find(class_="Price notranslate")
        sales_price = soup.find(class_="HistoricalPrice-promotion")
        if sales_price is None:
            price = re.findall(r'\d+.\d+', price.text)[0]
            return price, price
        else:
            original_price = re.findall(r'\d+.\d+', price.text)[0]
            sales_price = re.findall(r'\d+.\d+', sales_price.text)[0]
            return original_price, sales_price
    except (AttributeError, IndexError, TypeError):
        return None, None


def get_details(soup):
    try:
        details = soup.find(class_="ProductDescription-content").text
        composition = re.findall(re.compile(r'\w*:*\s*\d+%\s*\w*'), details)
        composition = [each.strip(' ') for each in composition]
        care = re.findall(re.compile(r'([Mm]achine [Ww]ash|[Ss]pecialist [Cc]lean [Oo]nly)'), details)
        details = re.split('\\.\s*|,\s*', details)
        details[:] = [each for each in details if each != "" and each not in composition and each not in care]
        return details, composition, care
    except (AttributeError, IndexError, TypeError):
        return None, None, None


def get_product_code_colour(soup):
    try:
        raw = soup.findAll(class_="ProductDescriptionExtras-item")
        colour = raw[0].text.split(': ')[1]
        code = raw[1].text.split(': ')[1]
        return colour, code
    except (AttributeError, IndexError, TypeError):
        return None, None


def get_image(soup):
    try:
        image = soup.find(class_='Carousel-image').get('srcset')
        image = image.split('.jpg')[0] + ".jpg"
        return image
    except (AttributeError, IndexError, TypeError):
        return None


def get_category(soup):
    category = ['Women']
    cat = soup.find(class_="ProductsBreadCrumbs").findAll('a')
    cat = [each.text for each in cat if each.text != "Home"]
    for each in cat:
        category.append(each)
    return category


def get_main_cats(url):
    url_list = []
    soup = make_soup(url)
    cats = soup.find(class_="MegaNav-categories").findAll('li')
    cats = [each.findAll('a') for each in cats]
    for each in cats:
        each_cat = [([ele.text], "https://www.topshop.com" + ele.get('href')) for ele in each]
        url_list.append(each_cat)

    priority_list = [url_list[2], url_list[3], url_list[4], url_list[5], url_list[1], url_list[6], url_list[0], url_list[7]]

    for each_list in priority_list:
        for each_cat in each_list:
            current_url = each_cat[1]
            print(current_url)
            soup = make_soup(current_url)
            link = ["https://www.topshop.com" + each.get('href') for each in soup.findAll(class_="Product-link")]
            # print(len(link), link)


def scrape(url_list):
    FINAL_OUTPUT = []
    for url in url_list:
        soup = make_soup(url)
        NAME = get_name(soup)
        ORI_PRICE, SALES_PRICE = get_price(soup)
        DETAILS, COMPOSITION, CARE = get_details(soup)
        COLOUR, CODE = get_product_code_colour(soup)
        IMAGE = get_image(soup)
        CATEGORY = get_category(soup)

        output = {
            "IMAGE": IMAGE,
            "BRAND": "TOPSHOP",
            "URL": url,
            "PRODUCT_CODE": CODE,
            "DETAILS": DETAILS,
            "ORIGINAL_PRICE": {
                "PRICE": ORI_PRICE,
                "CURRENCY": "Pound sterling"
            },
            "SALES_PRICE": {
                "PRICE": SALES_PRICE,
                "CURRENCY": "Pound sterling"
            },
            "COMPOSITION": COMPOSITION,
            "CARE_INSTRUCTION": CARE,
            "COLOUR": COLOUR,
            "CATEGORY": CATEGORY,
            "NAME": NAME
        }

        FINAL_OUTPUT.append(output)

    pretty_output = json.dumps(FINAL_OUTPUT, indent=3)
    print(pretty_output)


if __name__ == '__main__':
    urls = [
        "https://www.topshop.com/en/tsuk/product/clothing-427/dresses-442/green-check-taffeta-skater-dress-9502853",
        "https://www.topshop.com/en/tsuk/product/sale-6923952/shop-all-sale-6912866/bell-sleeve-chuck-on-dress-9163639",
        "https://www.topshop.com/uk/tsuk/product/36692642",
        "https://www.topshop.com/en/tsuk/product/bags-accessories-1702216/bags-purses-462/black-weave-cross-body-bag-9471126",
        "https://www.topshop.com/en/tsuk/product/jeans-6877054/mid-blue-jamie-jeans-9408806",
        "https://www.topshop.com/en/tsuk/product/shoes-430/boots-6909314/kacy-black-patent-chunky-boots-9508945",
        "https://www.topshop.com/en/tsuk/product/brands-4210405/adidas-6008354/purple-cuff-trackpants-by-adidas-9496189",
    "https://www.topshop.com/en/tsuk/product/shoes-430/villa-vegan-snake-print-boots-9387027"]
    # get_all_products(["https://www.topshop.com/en/tsuk/category/clothing-427?"])
    # scrape(urls)
    get_main_cats("https://www.topshop.com/")
