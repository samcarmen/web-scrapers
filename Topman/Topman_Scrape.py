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
    options.add_argument("User-Agent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                         "like Gecko) Chrome/79.0.3945.117 Safari/537.36'")
    driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\User\Downloads\chromedriver\chromedriver.exe")

    return driver


def make_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/79.0.3945.117 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    return soup


def get_name(soup):
    try:
        name_raw = soup.find(class_="ProductDetail-title")
        if name_raw is None:
            name = soup.find(class_="Bundles-title").text
            return name
        return name_raw.text
    except (AttributeError, IndexError, TypeError):
        return None


def get_price(soup):
    regex = r'\d+.\d+'
    try:
        bundle_price = soup.find(class_="Price Bundles-priceValue notranslate")
        if bundle_price is not None:
            price = re.findall(regex, bundle_price.text)
            return price, price
        else:
            price = soup.find(class_="Price notranslate")
            sales_price = soup.find(class_="HistoricalPrice-promotion")
            if sales_price is None:
                price = re.findall(regex, price.text)[0]
                return price, price
            else:
                original_price = re.findall(regex, price.text)[0]
                sales_price = re.findall(regex, sales_price.text)[0]
                return original_price, sales_price
    except (AttributeError, IndexError, TypeError):
        return None, None


def get_details(soup):
    care_example = r'([Mm]achine [Ww]ash|[Ss]pecialist [Cc]lean [Oo]nly)|[Hh]and [Ww]ash [Oo]nly|[Dd]ry [Cc]lean [Oo]nly)'

    raw_content = soup.find(class_="ProductDescription-content").findAll('li')
    raw_content_text = [each.text for each in raw_content]
    for each in raw_content_text:
        print(each)
        if re.match(re.compile(r'\d+:\s*\w+'), each):
            print(each)


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
        each_cat = [([ele.text], "https://www.topman.com" + ele.get('href')) for ele in each]
        url_list.append(each_cat[:-1])

    priority_list = [url_list[2], url_list[3], url_list[4], url_list[1], url_list[5], url_list[0],
                     url_list[6]]

    for each_list in priority_list:
        each_list = each_list[::-1]  # Reverse the list

        done_url = []
        for each_cat in each_list:
            stuck = 0
            current_url = each_cat[1]

            print("\nCurrently scrolling: ", current_url)

            if current_url in done_url:
                print("\nUh-oh, repeated url!", current_url)
                continue
            else:
                done_url.append(current_url)

            internal_visited = set()
            internal_list = []

            driver.get(current_url)
            driver.maximize_window()

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

                    link = [(each_cat[0], "https://www.topman.com" + each.get('href')) for each in
                            soup.findAll(class_="Product-link")]

                    for a, b in link:
                        if not b in internal_visited:
                            internal_visited.add(b)
                            internal_list.append((a, b))

                    print("Current length: ", len(internal_list))

                    if len(internal_list) >= total_links_available:
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
        try:
            print("\nCurrently scraping {}: {}".format(i, url))

            soup = make_soup(url)
            NAME = get_name(soup)
            ORI_PRICE, SALES_PRICE = get_price(soup)
            DETAILS, COMPOSITION, CARE = get_details(soup)
            COLOUR, CODE = get_product_code_colour(soup)
            IMAGE = get_image(soup)
            CATEGORY = get_category(soup)
            if small_cat[0] not in CATEGORY:
                CATEGORY.append(small_cat[0])

            output = {
                "IMAGE": IMAGE,
                "BRAND": "TOPMAN",
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

        except Exception as e:
            i += 1
            print(e, url)
            continue

        pretty_output = json.dumps(FINAL_OUTPUT, indent=3)

        with open('Topman_Data.json', 'w') as outfile:
            outfile.write(pretty_output)


if __name__ == '__main__':
    start = datetime.datetime.now()
    print("Start time: ", start)

    # all_urls = get_main_cats("https://www.topman.com/")
    #
    # done_all = datetime.datetime.now()
    # time = done_all - start
    # print("Time taken for getting all urls: ", int(time.total_seconds() / 60), "minutes")

    all_urls = [
                (["Blazers"], "https://www.topman.com/en/tmuk/product/clothing-140502/mens-blazers-5369753/black-skinny-fit-single-breasted-velvet-blazer-with-peak-lapels-8919955"),
                (["Shoes"], "https://www.topman.com/en/tmuk/product/shoes-and-accessories-1928527/trainers-8541034/white-drone-runner-trainers-9375713"),
                (["Suit"], "https://www.topman.com/en/tmuk/product/suits-1950628/double-breasted-suits-8611231/heritage-3-piece-black-check-skinny-fit-double-breasted-suit-with-peak-lapels-9275148")
                ]
    scrape(all_urls)

    end = datetime.datetime.now()
    print("End time: ", start)

    total = end - start
    print("Total time taken: ", int(total.total_seconds() / 60), "minutes")
