"""
You need to download a driver for Selenium to interface with your browser for the automate scrolling function.
Instruction to download: https://selenium-python.readthedocs.io/installation.html#drivers
Also, you need to change the executable path in automate_scrolling function to the path to your chromedriver.exe in your pc.

# The output for this program contains duplicate data #
"""
from bs4 import BeautifulSoup
import requests
import re
import json
import requests.exceptions
import time
from selenium import webdriver

output_list = []


def automate_scrolling():
    """
    Function to automate scrolling to tackle lazy loading website.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--incognito")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options,
                              executable_path=r"C:\Users\Carmen\Downloads\chromedriver_win32\chromedriver.exe")
    return driver


def get_all_url(url):
    """
    Function to get all URLs in a website.
    The links returned will be without duplicate.
    """
    new_urls = []

    driver = automate_scrolling()
    driver.get(url)

    y = 650
    for timer in range(0, 40):
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y += 1000
        time.sleep(1)  # Wait for one sec before scrolling
        page_source = driver.page_source
        my_soup = BeautifulSoup(page_source, 'html.parser')
        raw = my_soup.findAll(class_="title")
        for link in raw:
            tag = link.findAll('a')
            tag = "https://www.esprit.com.my" + tag[0].get('href')
            print(tag)
            new_urls.append(tag)

    print("Number of URLs: ", len(set(new_urls)))
    return list(set(new_urls))


def make_soup(url):
    # Make a GET request to fetch the raw HTML content
    page = requests.get(url)
    # Parse the html content
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    return soup


def get_image(url):
    """
    Function to get the image of a product.
    Use automate scrolling since the page is lazy loaded.
    """
    driver = automate_scrolling()
    driver.get(url)
    driver.execute_script("window.scrollTo(0, 650);")
    time.sleep(0.5)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    try:
        image = soup.find_all('img', class_='detail-pic')
        image_src = image[0].get('src')
        image_url = re.findall(r'[\S]+.jpg', image_src)
        print("Here you go: ", image_url)
        image_string = image_url[0]
        return image_string
    except:
        print("IMAGE RETRIEVAL FAILED: ", url)


def get_product_code(url):
    """
    Function to return the unique product code of a product
    """
    soup = make_soup(url)
    try:
        product_code = soup.find(class_="product-code ls025").text
        return product_code
    except:
        print("PRODUCT CODE RETRIEVAL FAILED: ", url)


def get_description(url):
    """
    Function to return a list of description about a product.
    """
    my_soup = make_soup(url)
    all_description = my_soup.findAll(class_="item-desc")
    try:
        description = [item.text.strip("\n") for item in all_description]
        return description if len(description) else None
    except:
        print("DESCRIPTION RETRIEVAL FAILED: ", url)


def get_price(url):
    """
    Function to get the original and discounted price of a product.
    Regex is used to separate the currency and the price.
    Returns a price list which consists of [currency, original_price, discounted_price]
    """
    price_list = []
    my_soup = make_soup(url)

    try:
        this_item_price = my_soup.findAll(class_="option-board cp-col-xs-24 cp-col-sm-24 cp-col-md-10")
        discounted_price = this_item_price[0]
        discounted = discounted_price.find(class_="money-amount sale-price").text

        original_price = this_item_price[0].find(class_="money-amount list-price price-off")
        if original_price is not None:
            original = original_price.text
        else:  # The original price is the discounted price if there is no original price
            original = discounted

        currency_regex = re.compile(r'\D+')
        price_regex = re.compile(r'\d+\D+\d+')

        # Find the price and currency using regex
        # A list is returned by findall function hence the first item from the list is retrieved
        currency = currency_regex.findall(original)[0]
        ori_price = price_regex.findall(original)[0]
        disc_price = price_regex.findall(discounted)[0]

        price_list.append(currency)
        price_list.append(ori_price)
        price_list.append(disc_price)

        return price_list

    except:
        print("PRICE RETRIEVAL FAILED: ", url)


def get_colour(url):
    """
    Function to return all colours available for a product
    All colours will be stored in a list
    """
    my_soup = make_soup(url)
    try:
        all_colour = my_soup.findAll(class_="thumb")
        colour = [item['alt'] for item in all_colour]  # You need a list for the iteration, so don't use index 0
        return colour
    except:
        print("COLOUR RETRIEVAL FAILED: ", url)


def get_category(url):
    """
    Function to return the category of each item, e.g. WOMEN -> CLOTHES -> Dresses
    """
    my_soup = make_soup(url)
    try:
        all_category = my_soup.select(".cp-breadcrumb__item .cp-breadcrumb__text")
        category = [item.text for item in all_category]
        return category
    except:
        print("CATEGORY RETRIEVAL FAILED: ", url)


def get_washing_guide(url):
    """
    Function to return a list of washing guide for a product.
    """
    my_soup = make_soup(url)
    try:
        washing_guide = my_soup.select(".washing-guides .guide-item")
        guide = [item['title'] for item in washing_guide]  # list comprehension
        return guide if len(guide) else None
    except:
        print("WASHING GUIDE RETRIEVAL FAILED: ", url)


def get_name(url):
    """
    Function to return the name of a product.
    """
    my_soup = make_soup(url)
    try:
        name = my_soup.find('h1', {'class': 'headline ls025'}).text
        return name
    except:
        print("NAME RETRIEVAL FAILED: ", url)


def scrape_each_url(url_list):
    """
    Function to scrape the information for every url retrieved from a website.
    The information for each product will be appended to an output list.
    """
    for each_url in url_list:
        try:
            currency = get_price(each_url)[0]
            ori_price = get_price(each_url)[1]
            discounted_price = get_price(each_url)[2]
        except:
            print("PRICE RETRIEVAL FAILED", each_url)
        image = get_image(each_url)
        product_code = get_product_code(each_url)
        description = get_description(each_url)
        colour = get_colour(each_url)
        category = get_category(each_url)
        washing_guide = get_washing_guide(each_url)
        name = get_name(each_url)

        output_json = {"IMAGE": image,
                       "PRODUCT_CODE": product_code,
                       "BRAND": "ESPRIT",
                       "URL": each_url,
                       "Category": category,
                       "DESCRIPTION": {
                           "Description": description,
                           "Colour": colour,
                           "Washing Guide": washing_guide
                       },
                       "ORIGINAL_PRICE": {
                           "Price": ori_price,
                           "Currency": currency
                       },
                       "DISCOUNTED_PRICE": {
                           "Price": discounted_price,
                           "Currency": currency
                       },
                       "NAME": name
                       }

        output_list.append(output_json)


if __name__ == "__main__":
    url_list = "https://www.esprit.com.my/product/SALE_ACCESSORIES/list.html"
    all_url = get_all_url(url_list)
    scrape_each_url(all_url)

    with open('raw_scrape_esprit.json', 'w') as outfile:
        json.dump(output_list, outfile)

    with open("raw_scrape_esprit.json", 'r') as json_file:
        parsed = json.load(json_file)

    pretty_output = json.dumps(parsed, indent=2)
    print(pretty_output)

    f = open("SALE_ACCESSORIES.json", "w")
    f.write(pretty_output)
    f.close()

#########################EXTRA INFO#########################
"""
MEN_CLOTHES -> https://www.esprit.com.my/product/MEN_CLOTHES/list.html
            -> 234

MEN_SHOP_BY_TREND -> https://www.esprit.com.my/product/MEN_SHOP%20BY%20TREND/list.html
                  -> 60

WOMEN_CLOTHES -> https://www.esprit.com.my/product/WOMEN_CLOTHES/list.html
              -> 219

WOMEN_SHOP_BY_TREND -> https://www.esprit.com.my/product/WOMEN_SHOP%20BY%20TREND/list.html
                    -> 137

ACCESSORIES_WOMEN -> https://www.esprit.com.my/product/ACCESSORIES_WOMEN/list.html
                  -> 78

ACCESSORIES_MEN -> https://www.esprit.com.my/product/ACCESSORIES_MEN/list.html
                -> 36
                
SALE_WOMEN -> https://www.esprit.com.my/product/SALE_WOMEN/list.html
           -> 127

SALE_MAN -> https://www.esprit.com.my/product/SALE_MEN/list.html
         -> 172

SALE_ACCESSORIES -> https://www.esprit.com.my/product/SALE_ACCESSORIES/list.html
                 -> 75           
"""
