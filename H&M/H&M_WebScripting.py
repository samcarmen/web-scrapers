# Scrape until shirt

import json
import re
import time
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import Request, urlopen
from selenium.common.exceptions import NoSuchElementException
import timeit
from plyer import notification

output = []
# 100 items 7 minutes


def get_all_url(url):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--incognito")
    options.add_argument("--window-size=1920x1080")
    # options.add_argument("--headless")
    options.add_argument(
        "User-Agent:'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'")
    driver = webdriver.Chrome(chrome_options=options,
                              executable_path=r"C:\Users\user\Downloads\chromedriver_win32\chromedriver.exe")
    driver.get(url)
    driver.find_element_by_xpath('//*[@title="Choose Malaysia as your region"]').click()
    time.sleep(1)
    driver.find_element_by_class_name("menu__super-link").click()
    driver.find_element_by_link_text("Shirts & Blouses").click()
    driver.find_element_by_link_text("Shirts").click()

    while True:
        try:
            driver.find_element_by_xpath("//button[contains(.,'Load More Products')]").click()
            time.sleep(5)
        except Exception as e:
            print(e)
            break

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    url_list = []
    url_container = soup.findAll(class_="product-item")
    small_container = [container.findAll('a', class_="item-link") for container in url_container]
    for i in range(len(small_container)):
        url_list.append("https://www2.hm.com" + small_container[i][0].get('href'))
    print(len(set(url_list)))
    print(len(url_list))
    return url_list


def make_soup(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, "html.parser")
    return soup


def get_image(url):
    soup = make_soup(url)
    raw = soup.find(class_="pdp-image product-detail-images product-detail-main-image")
    img = raw.find('img').get('src')
    return img


def get_all_description(url):
    description_list = {}
    soup = make_soup(url)
    raw = soup.find(class_="pdp-drawer-content pdp-details-content")
    details_headline = raw.findAll(class_="details-headline")
    containers = raw.findAll(class_="details-list")
    for i in range(len(containers)):
        headline = details_headline[i].text
        each_detail = containers[i].findAll(class_="details-list-item")
        description = [item.text for item in each_detail]
        description_list[headline.capitalize()] = description
    return description_list


def get_price(url):
    soup = make_soup(url)
    price = soup.find(class_="price-value").text.lstrip()
    original = soup.find(class_="js-price-value-original price-value-original")
    currency = re.findall('[a-zA-Z]+', price)[0]
    price = re.findall('\d+\.\d+', price)[0]

    if original is None:
        return currency, price, price
    else:
        original_price = re.findall('\d+\.\d+', original.text.lstrip())[0]
        return currency, price, original_price


# def get_category(url):
#     soup = make_soup(url)
#     pattern = re.compile((r'"category"'))
#     script = soup.find("script", text=pattern)
#     data = json.loads(script.get_text())
#     category = data['category']['name']
#     return category


def get_name(url):
    soup = make_soup(url)
    name = soup.find(class_="primary product-item-headline").text
    name = name.lstrip()  # remove leading whitespace
    return name


def scrape(url_list):
    output_list = []
    category = ["Women", "Shirts & Blouses", "Shirts"]
    for url in url_list:
        image = get_image(url)
        description = get_all_description(url)
        price = get_price(url)
        name = get_name(url)
        output = {"IMAGE": image,
                  "BRAND": "H&M",
                  "URL": url,
                  "DESCRIPTION": description,
                  "ORIGINAL_PRICE": {
                      "Price": price[2],
                      "Currency": price[0]
                  },
                  "SALES_PRICE": {
                      "Price": price[1],
                      "Currency": price[0]
                  },
                  "CATEGORY": category,
                  "NAME": name
                  }
        output_list.append(output)

    return output_list


if __name__ == "__main__":
    start = time.time()
    url = "https://www2.hm.com/en_asia4/productpage.0800084001.html"
    URL_LIST = get_all_url(url)
    OUTPUT_LIST = scrape(URL_LIST)

    with open('H&M_Raw_Data.json', 'w') as outfile:
        json.dump(OUTPUT_LIST, outfile)

    with open("H&M_Raw_Data.json", 'r') as json_file:
        parsed = json.load(json_file)

    pretty_output = json.dumps(parsed, indent=2)
    print(pretty_output)

    f = open("H&M_Data_Temp.json", "w")
    f.write(pretty_output)
    f.close()

    end = time.time()
    time_taken = (end - start) / 60  # in minute
    print("Time taken: ", time_taken, " minutes")

    notification.notify(
        title='Meow~',
        message='The scraping is done!',
        app_icon=None,  # e.g. 'C:\\icon_32x32.ico'
        timeout=10,  # seconds
    )
