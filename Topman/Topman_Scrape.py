from bs4 import BeautifulSoup
import datetime
import json
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


def initialise_web_driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--incognito")
    options.add_argument("User-Agent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'")
    driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\User\Downloads\chromedriver\chromedriver.exe")

    return driver


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
    try:
        category = ['Women']
        cat = soup.find(class_="ProductsBreadCrumbs").findAll('a')
        cat = [each.text for each in cat if each.text != "Home"]
        for each in cat:
            category.append(each)
        return category
    except (AttributeError, IndexError, TypeError):
        return None


def get_main_cats(url):
    driver = initialise_web_driver()

    url_list = []
    all_url = []
    visited = set()  # Unique set of urls for scraping later

    soup = make_soup(url)
    main_cats = soup.find(class_="MegaNav-categories").findAll('li')
    cats = [each.findAll('a') for each in main_cats]

    for each in cats:
        each_cat = [([ele.text], "https://www.topshop.com" + ele.get('href')) for ele in each]
        url_list.append(each_cat[:-1])

    priority_list = [url_list[2], url_list[3], url_list[4], url_list[1], url_list[5], url_list[0],
                     url_list[6]]

    for each_list in priority_list:
        each_list = each_list[::-1]  # Reverse the list

        for each_cat in each_list:
            current_url = each_cat[1]

            if current_url == "https://www.topshop.com/en/tsuk/category/brands-4210405/dresses/N-7z2Zqn9Zdgl":
                print("\nRemoved")
                continue
            print("\nCurrently scrolling: ", current_url)

            internal_visited = set()
            internal_list = []

            driver.get(current_url)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')

            try:
                total_links_available = soup.find(class_="Filters-totalResults").text
                total_links_available = int(re.findall(re.compile(r'\d+'), total_links_available)[0])
                print("Total links available: ", total_links_available)

                while True:
                    driver.find_element_by_tag_name('body').send_keys(Keys.END)
                    time.sleep(3)
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, 'lxml')

                    link = [(each_cat[0], "https://www.topshop.com" + each.get('href')) for each in
                            soup.findAll(class_="Product-link")]

                    for a, b in link:
                        if not b in internal_visited:
                            internal_visited.add(b)
                            internal_list.append((a, b))

                    print("Current length: ", len(internal_list))

                    if len(internal_list) >= total_links_available-1:
                        for a, b in internal_list:
                            if not b in visited:
                                visited.add(b)
                                all_url.append((a, b))
                        print("Final length after scrolling:", len(all_url))
                        break

            except (AttributeError, IndexError, TypeError):
                continue

    print("Final final length: ", len(all_url))
    for each in all_url:
        print(each)
    return all_url


def scrape(url_list):
    FINAL_OUTPUT = []
    i = 1

    for small_cat, url in url_list:
        print("Currently scraping {}: {}".format(i, url))

        soup = make_soup(url)
        NAME = get_name(soup)
        ORI_PRICE, SALES_PRICE = get_price(soup)
        DETAILS, COMPOSITION, CARE = get_details(soup)
        COLOUR, CODE = get_product_code_colour(soup)
        IMAGE = get_image(soup)
        CATEGORY = get_category(soup)
        if small_cat not in CATEGORY:
            CATEGORY.append(small_cat)

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

        i += 1
        FINAL_OUTPUT.append(output)

    pretty_output = json.dumps(FINAL_OUTPUT, indent=3)

    with open ('Topman_Data.json', 'w') as outfile:
        outfile.write(pretty_output)


if __name__ == '__main__':
    start = datetime.datetime.now()
    print("Start time: ", start)

    all_urls = get_main_cats("https://www.topman.com/")

    done_all = datetime.datetime.now()
    time = done_all - start
    print("Time taken for getting all urls: ", int(time.total_seconds() / 60), "minutes")

    scrape(all_urls)

    end = datetime.datetime.now()
    print("End time: ", start)

    total = end - start
    print("Total time taken: ", int(total.total_seconds() / 60), "minutes")
