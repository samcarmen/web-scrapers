from bs4 import BeautifulSoup as BS
import datetime
import json
import re
import requests
from selenium import webdriver
import time

from selenium.webdriver.chrome.options import Options


def make_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BS(page.content, 'lxml')
    return soup


def get_name(soup):
    try:
        name = soup.find(id="goodsNmArea")
        name = name.find('span').text.lstrip('\n ').rstrip(' \n')
        return name
    except (TypeError, AttributeError, IndexError):
        return None


def get_product_code(soup):
    try:
        product_code = soup.find(class_="number").find('span').text
        return product_code
    except (TypeError, AttributeError, IndexError):
        return None


def get_price(soup):
    try:
        special_price = soup.find(id="product-price-7").text
        old_price = soup.find(id="old-price-7").text
        pattern = re.compile(r'\d+.\d+')
        special_price = re.search(pattern, special_price).group(0)

        if old_price == "":
            return special_price, special_price
        else:
            pattern = re.compile(r'\d+.\d+')
            special_price = re.search(pattern, special_price).group(0)
            old_price = re.search(pattern, old_price).group(0)
            return old_price, special_price
    except (TypeError, AttributeError, IndexError):
        print("None")
        return None, None


def get_image(soup):
    try:
        image = soup.find(id="prodImgDefault").find('img')
        return image.get('src')
    except (TypeError, AttributeError, IndexError):
        print("Error retrieving image")
        return None


def get_details(soup):
    try:
        description = soup.find(class_="content con-wdt")
        text = description.text.lstrip('\n ')
        pattern = re.compile(r'.+')
        filtered_text = re.findall(pattern, text)
        description = re.split('\.|_|- |!', filtered_text[0])
        description = [each.lstrip(' ') for each in description if each.lstrip(' ') != ""]
        material = re.findall(re.compile(r'\d+%\s*[a-zA-Z]+'), filtered_text[2])
        care = filtered_text[4].split(',')
        care = [each.lstrip(' ') for each in care]

        return description, material, care
    except (AttributeError, TypeError, IndexError):
        return None, None, None


def get_colour(soup):
    try:
        colour = soup.find(id="colorNmId").text
        pattern = re.compile(r'\w+:\w+\d+')
        colour = re.split(pattern, colour)[1].strip(' ')
        return colour
    except:
        return None


def get_category(soup):
    try:
        category = soup.find('div', class_="breadcrumbs")
        span = category.findAll('span')
        category = [each.text for each in span]
        category.remove(str(get_name(soup)))
        return category
    except:
        return None


def get_all_category(soup):
    main_cat = soup.findAll(class_="cateNaviLink")
    sub = [each.find('a').get('href') for each in main_cat]
    print(len(sub))
    return sub


def get_each_product(cat_list):
    url_list = []
    for each in cat_list:
        print("Currently processing: ", each)
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--incognito")
        options.add_argument("User-Agent:'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'")
        driver = webdriver.Chrome(options=options,
                                  executable_path=r"C:\Users\Carmen\Downloads\chromedriver_win32\chromedriver.exe")
        driver.get(each)
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            page_source = driver.page_source
            soup = BS(page_source, 'html.parser')

            raw = soup.findAll(class_="product-name")
            links = [each.find('a').get('href') for each in raw]
            for each in links:
                url_list.append(each)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        print("length of list: ", len(url_list))
    print("Total number of url:", len(set(url_list)))
    driver.quit()
    return set(url_list)


def scrape(url_list):
    ALL_OUTPUT = []
    i = 1
    for url in url_list:
        print("Currently processing url {}: {}".format(i, url))
        soup = make_soup(url)
        IMAGE = get_image(soup)
        NAME = get_name(soup)
        CODE = get_product_code(soup)
        ORI_PRICE, SALES_PRICE = get_price(soup)
        DESCRIPTION, MATERIAL, CARE = get_details(soup)
        COLOUR = get_colour(soup)
        CATEGORY = get_category(soup)

        output = {
            "IMAGE": IMAGE,
            "BRAND": "UNIQLO",
            "URL": url,
            "PRODUCT_CODE": CODE,
            "DESCRIPTION": DESCRIPTION,
            "MATERIAL": MATERIAL,
            "CARE": CARE,
            "SALES_PRICE": {
                "PRICE": SALES_PRICE,
                "CURRENCY": "RM"
            },
            "ORIGINAL_PRICE": {
                "PRICE": ORI_PRICE,
                "CURRENCY": "RM"
            },
            "COLOUR": COLOUR,
            "CATEGORY": CATEGORY,
            "NAME": NAME
        }
        ALL_OUTPUT.append(output)
        i += 1

    pretty_output = json.dumps(ALL_OUTPUT, indent=3)
    with open('Uniqlo_Data.json', 'w') as file:
        file.write(pretty_output)


if __name__ == '__main__':
    START = datetime.datetime.now()
    print("Start time: ", START)

    main_page = "https://www.uniqlo.com/my/store/"
    main_soup = make_soup(main_page)
    all_cat = get_all_category(main_soup)
    all_product = get_each_product(all_cat)
    scrape(all_product)

    END = datetime.datetime.now()
    print("End time: ", START)

    total = END - START
    print("Total time taken: ", int(total.total_seconds() / 60), "minutes")


"""
10.1.2020

20:33
length of list:  6371
Total number of url: 1722

21:19
length of list:  6443
Total number of url: 1722
"""