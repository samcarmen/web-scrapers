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
        pattern = re.compile(r'\d+% \w+')
        for each in details:
            if re.match(pattern, each):
                print("yes")
            else:
                print('no')
        details = re.split('\\. |\\.', details)
        details[:] = [each for each in details if each != ""]
        return details
    except (AttributeError, IndexError, TypeError):
        return None


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


def scrape(url_list):
    FINAL_OUTPUT = []
    for url in url_list:
        soup = make_soup(url)
        NAME = get_name(soup)
        ORI_PRICE, SALES_PRICE = get_price(soup)
        DETAILS = get_details(soup)
        COLOUR, CODE = get_product_code_colour(soup)
        IMAGE = get_image(soup)

        output = {
            "IMAGE": IMAGE,
            "BRAND": "TOPSHOP",
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
            "COLOUR": COLOUR,
            "NAME": NAME
        }

        FINAL_OUTPUT.append(output)

    pretty_output = json.dumps(FINAL_OUTPUT, indent=3)
    # print(pretty_output)


if __name__ == '__main__':
    url_list = ["https://www.topshop.com/en/tsuk/product/clothing-427/dresses-442/green-check-taffeta-skater-dress-9502853",
                "https://www.topshop.com/en/tsuk/product/sale-6923952/shop-all-sale-6912866/bell-sleeve-chuck-on-dress-9163639"]
    scrape(url_list)

