from bs4 import BeautifulSoup
import requests
import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import Request, urlopen
from selenium.common.exceptions import NoSuchElementException
import time
from plyer import notification

OUTPUT_LIST = []

def get_all_url(url):
    options = Options()

    # options.add_argument("--headless")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--incognito")
    options.add_argument("User-Agent:'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'")
    options.add_argument("--window-size=1382,744")
    driver = webdriver.Chrome(chrome_options=options,
                              executable_path=r"C:\Users\user\Downloads\chromedriver_win32\chromedriver.exe")
    for each in url:
        cat = get_category(each)
        driver.get(each)
        # driver.maximize_window()
        # print(driver.get_window_size())
        page_no = 1
        url_list = []

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        container = soup.findAll(class_="name-link")
        urls = [link.get('href') for link in container]
        for each_url in urls:
            url_list.append(each_url)
        time.sleep(5)
        while True:
            try:
                page_no += 1
                new_class_name = "page-" + str(page_no)
                driver.find_element_by_class_name(new_class_name).click()
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                container = soup.findAll(class_="name-link")
                urls = [link.get('href') for link in container]
                for each_url in urls:
                    url_list.append(each_url)
                time.sleep(5)
            except Exception as e:
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                container = soup.findAll(class_="name-link")
                urls = [link.get('href') for link in container]
                for each_url in urls:
                    url_list.append(each_url)
                print(e)
                break
        print(len(set(url_list)))
        scrape(set(url_list), cat)

    with open('CottonOn_Raw_Data.json', 'w') as outfile:
        json.dump(OUTPUT_LIST, outfile)

    with open("CottonOn_Raw_Data.json", 'r') as json_file:
        parsed = json.load(json_file)

    pretty_output = json.dumps(parsed, indent=2)
    print(pretty_output)

    f = open("CottonOn_Data_Temp.json", "w")
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


def make_soup(url):
    # Make a GET request to fetch the raw HTML content
    page = requests.get(url)
    # Parse the html content
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    return soup


def get_image(url):
    soup = make_soup(url)
    try:
        image = soup.find(class_="media-source").get("src")
        image_url = re.findall(r'[\S]+.jpg', image)
        return image_url[0]
    except (TypeError, IndexError):
        print("IMAGE RETRIEVAL FAILED: ", url)


def get_price(url):
    """
    if standard price is None, original price is price sales
    """
    soup = make_soup(url)
    price = soup.find(class_="price-standard")
    if price is None:
        price = soup.find(class_="price-sales")
        currency = re.findall('[a-zA-Z]+', price.text)
        price = re.findall('\d+\.\d+', price.text)
        return currency, price, price
    else:
        sales_price = soup.find(class_="price-sales")
        sales_price = re.findall('\d+\.\d+', sales_price.text)
        standard_price = re.findall('\d+\.\d+', price.text)
        currency = re.findall('[a-zA-Z]+', price.text)
        return currency, standard_price, sales_price


def get_product_code(url):
    soup = make_soup(url)
    try:
        product_code = soup.findAll(class_="product-code")[0].text
        return product_code
    except (AttributeError, IndexError, TypeError):
        print("PRODUCT CODE RETRIEVAL FAILED: ", url)


def get_name(url):
    soup = make_soup(url)
    try:
        name = soup.findAll(class_="product-name")[0].text
        return name
    except IndexError:
        print("NAME RETRIEVAL FAILED: ", url)


def get_colour(url):
    soup = make_soup(url)
    try:
        colour = soup.find(id="selected-color-value").text
        return colour
    except (AttributeError, TypeError):
        print("COLOUR RETRIEVAL FAILED: ", url)


def get_composition(url):
    soup = make_soup(url)
    description = soup.findAll(id="details-description-container")
    string = [item.text for item in description]
    container = re.split(r'Composition:', string[0])
    try:
        composition = container[1]
        composition = composition.rstrip('\n')
        composition = composition.lstrip()
        return composition
    except:
        return []


def get_feature(url):
    soup = make_soup(url)
    description = soup.findAll(id="details-description-container")
    string = [item.text for item in description]
    feature = re.split("Composition:", string[0])
    feature = re.split("Features:", feature[0])
    try:
        feature = [i.lstrip() for i in feature]
        feature = [i.rstrip() for i in feature]
        final_feature = feature[1]
        feature = final_feature.split('\n')
        feature_list = [each.lstrip('-') for each in feature]
        feature_list = [each.lstrip() for each in feature_list]
        feature_list = [each.lstrip('-') for each in feature_list]
        feature_list = [each.rstrip() for each in feature_list]
        return feature_list
    except:
        return []


def get_category(url):
    category = url.split('https://cottonon.com/MY/kids/kids-boys-1-8/boys-1-8-')
    return category[1].rstrip('/')


def scrape(url_list, cat):
    for url in url_list:
        image = get_image(url)
        code = get_product_code(url)
        colour = get_colour(url)
        price = get_price(url)
        composition = get_composition(url)
        feature = get_feature(url)
        name = get_name(url)
        category = ["Kids & Baby", "Boys"]
        category.append(cat)
        output = {
            "IMAGE": image,
            "PRODUCT_CODE": code,
            "BRAND": "Cotton On",
            "URL": url,
            "FEATURES": feature,
            "COMPOSITION": composition,
            "ORIGINAL_PRICE": {
                "PRICE": price[1][0],
                "CURRENCY": price[0][0]
            },
            "SALES_PRICE": {
                "PRICE": price[2][0],
                "CURRENCY": price[0][0]
            },
            "CATEGORY": category,
            "COLOUR": colour,
            "NAME": name
        }

        OUTPUT_LIST.append(output)


if __name__ == "__main__":
    start = time.time()
    URL = []
    url_1 = "https://cottonon.com/MY/kids/kids-boys-1-8/boys-1-8-tops-t-shirts/"
    url_2 = "https://cottonon.com/MY/kids/kids-boys-1-8/boys-1-8-polos-shirts/"
    url_3 = "https://cottonon.com/MY/kids/kids-boys-1-8/boys-1-8-shorts/"
    url_4 = "https://cottonon.com/MY/kids/kids-boys-1-8/boys-1-8-pants/"
    url_5 = "https://cottonon.com/MY/kids/kids-boys-1-8/boys-1-8-jackets-knitwear/"
    url_6 = "https://cottonon.com/MY/kids/kids-boys-1-8/boys-1-8-swimwear/"
    url_7 = "https://cottonon.com/MY/kids/kids-boys-1-8/boys-1-8-sleepwear/"
    url_8 = "https://cottonon.com/MY/kids/kids-boys-1-8/boys-1-8-shoes/"
    url_9 = "https://cottonon.com/MY/kids/kids-boys-1-8/boys-1-8-socks-underwear/"
    url_10 = "https://cottonon.com/MY/kids/kids-boys-1-8/boys-1-8-accessories/"
    url_11 = "https://cottonon.com/MY/kids/kids-boys-1-8/boys-1-8-fleece/"

    URL.append(url_1)
    URL.append(url_2)
    URL.append(url_3)
    URL.append(url_4)
    URL.append(url_5)
    URL.append(url_6)
    URL.append(url_7)
    URL.append(url_8)
    URL.append(url_9)
    URL.append(url_10)
    URL.append(url_11)

    url_list = get_all_url(URL)




