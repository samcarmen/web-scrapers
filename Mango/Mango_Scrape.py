import json
from plyer import notification
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
import re
import time


def initialise_web_driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--incognito")
    options.add_argument("User-Agent:'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'")
    options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=options,
                              executable_path=r"C:\Users\User\Downloads\chromedriver_win32\chromedriver.exe")

    return driver


def make_soup(driver, url):
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    return soup


def get_all_url(soup):
    """
    Function to get all the main links of each category on the Women main page
    :param soup:
    :return: a list of urls which comprised of each category in Women clothing and accessories
    """
    clothing_container = soup.find('nav', {"aria-label": "Filter by Girls"})
    container = clothing_container.findAll('a')
    urls = [each.get('href') for each in container]
    urls = ["https://shop.mango.com" + each for each in urls]
    url_list = [url for url in urls]  # append the url to a new list

    accessories_container = soup.find('nav', {"aria-label": "Filter by Accessories"})
    container = accessories_container.findAll('a')
    urls = [each.get('href') for each in container]
    urls = ["https://shop.mango.com" + each for each in urls]
    for url in urls:
        url_list.append(url)

    # add the left out ones into the list
    # url_list.append("https://shop.mango.com/my/plus-size/clothing_c48777000")

    return url_list


def scroll_each_url(url_list):
    """
    Function to retrieve the link of every item in each category
    by scrolling to the very bottom of the page.
    :param url_list:
    :return:
    """
    all_url = []

    for i in range(len(url_list)):
        print("Processing url: ", i)
        url = url_list[i]

        driver = initialise_web_driver()
        driver.get(url)  # open a new page

        try:
            driver.find_element_by_id("navColumns4").click()
        except (NoSuchElementException, ElementClickInterceptedException):
            pass

        SCROLL_PAUSE_TIME = 4

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Get the urls of the item
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            found_url = soup.findAll('a', class_="aZ-72")
            found_url = [each.get('href') for each in found_url]
            found_url = ["https://shop.mango.com" + each for each in found_url]

            for each in found_url:
                all_url.append(each)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                driver.close()
                break
            last_height = new_height

    print("all_url: ", len(all_url))
    print("set_url: ", len(set(all_url)))

    all_url_list = [each for each in set(all_url)]
    return all_url_list


def get_name(soup):
    try:
        name = soup.find(class_="product-name").text
        return name
    except (TypeError, AttributeError, IndexError):
        print("*Error retrieving name")


def get_price(soup):
    price_list = []
    regex = r"([a-zA-Z]+)(\d+)"

    try:
        sales_container = soup.find(class_="product-sale").text
        standard_container = soup.find(class_="product-sale--cross")

        if standard_container is None:
            standard_container = sales_container
        else:
            standard_container = standard_container.text

        sales_match = re.search(regex, sales_container)
        standard_match = re.search(regex, standard_container)

        currency = sales_match.group(1)
        sales_price = sales_match.group(2)
        standard_price = standard_match.group(2)

        price_list.append(currency)
        price_list.append(sales_price)
        price_list.append(standard_price)

        return price_list

    except (TypeError, AttributeError, IndexError):
        print("*Error retrieving price")


def get_category(soup):
    try:
        container = soup.findAll(class_="breadcrumbs-link")
        span = [each.findAll('span') for each in container]
        category = [each[0].text for each in span]
        return category
    except (TypeError, AttributeError, IndexError):
        print("*Error retrieving category*")


def get_colour(soup):
    try:
        colour = soup.find(class_="colors-info-name").text
        return colour
    except (TypeError, AttributeError, IndexError):
        print("*Error retrieving colour")


def get_description(soup):
    try:
        container = soup.findAll(class_="product-info-text")[0].text
        description = container.split('. ')
        return description
    except (TypeError, AttributeError, IndexError):
        print("*Error retrieving description")


def get_material(soup):
    try:
        container = soup.findAll(class_="product-info-block")[1]
        composition = container.find(class_="product-info-text").text
        composition = composition.split('.')
        # composition = [each.split(':') for each in composition]
        return composition
    except (TypeError, AttributeError, IndexError):
        print("*Error retrieving material")


def get_washing_instruction(soup):
    try:
        container = soup.find(class_="product-info-icons")
        if container is None:
            return []
        instruction = [each.get('alt') for each in container]
        instruction = [each.lower() for each in instruction]
        return instruction
    except (TypeError, AttributeError, IndexError):
        print("*Error retrieving washing instruction")


def get_image(soup):
    try:
        name = soup.find('h1', class_="product-name").text
        name = name + " - Article without model"
        container = soup.find('img', alt=name)
        image = container.get('src')
        image_url = re.findall(r'[\S]+.jpg', image)
        return image_url[0]

    except (TypeError, AttributeError, IndexError):
        try:
            container = soup.find('img', class_="image-1 image-js")
            image = container.get('src')
            image_url = re.findall(r'[\S]+.jpg', image)
            return image_url
        except (TypeError, AttributeError, IndexError):
            print("*Error retrieving image")


def get_product_reference(soup):
    try:
        ref = soup.find(class_="product-reference").text
        return ref
    except (TypeError, AttributeError, IndexError):
        print("*Error retrieving product reference")


def scrape_all(url_list):
    output_list = []
    driver = initialise_web_driver()
    for i in range(len(url_list)):
        url = url_list[i]
        print("Now processing: ", i + 1, url)

        soup = make_soup(driver, url)

        image = get_image(soup)
        ref = get_product_reference(soup)
        colour = get_colour(soup)
        price = get_price(soup)

        try:
            currency = price[0]
            original_price = price[2]
            sales_price = price[1]
        except (TypeError, AttributeError, IndexError):
            currency = []
            original_price = []
            sales_price = []

        description = get_description(soup)
        material = get_material(soup)
        instruction = get_washing_instruction(soup)
        name = get_name(soup)
        category = get_category(soup)

        output = {
            "IMAGE": image,
            "PRODUCT_REFERENCE": ref,
            "BRAND": "Mango",
            "URL": url,
            "DESCRIPTION": description,
            "MATERIAL": material,
            "ORIGINAL_PRICE": {
                "PRICE": original_price,
                "CURRENCY": currency
            },
            "SALES_PRICE": {
                "PRICE": sales_price,
                "CURRENCY": currency
            },
            "WASHING_INSTRUCTION": instruction,
            "CATEGORY": category,
            "COLOUR": colour,
            "NAME": name
        }
        output_list.append(output)

    return output_list


def write_to_file(output):
    with open('raw_scrape_mango.json', 'w') as outfile:
        json.dump(output, outfile)

    with open("raw_scrape_mango.json", 'r') as json_file:
        parsed = json.load(json_file)

    pretty_output = json.dumps(parsed, indent=2)
    print(pretty_output)

    f = open("Mango_Data_Temp.json", "w")
    f.write(pretty_output)
    f.close()


if __name__ == "__main__":
    start = time.time()

    women_url = "https://shop.mango.com/my/girls/coats_c10792813"

    # women_driver = initialise_web_driver()
    # women_soup = make_soup(women_driver, women_url)
    #
    all_women_category = ['https://shop.mango.com/my/girls/coats_c10792813', 'https://shop.mango.com/my/girls/coats-quilted-coats_c11610759', 'https://shop.mango.com/my/girls/coats-coats_c11277498', 'https://shop.mango.com/my/girls/coats-gilets_c16989719', 'https://shop.mango.com/my/girls/coats-faux-fur_c15758657', 'https://shop.mango.com/my/girls/jackets_c10281700', 'https://shop.mango.com/my/girls/dresses_c11805879', 'https://shop.mango.com/my/girls/jumpsuits_c56982220', 'https://shop.mango.com/my/girls/cardigans-and-sweaters_c19557162', 'https://shop.mango.com/my/girls/sweatshirts_c47703127', 'https://shop.mango.com/my/girls/shirts_c18370679', 'https://shop.mango.com/my/girls/t-shirts_c19045604', 'https://shop.mango.com/my/girls/trousers_c16674009', 'https://shop.mango.com/my/girls/leggings_c33314338', 'https://shop.mango.com/my/girls/jeans_c15188815', 'https://shop.mango.com/my/girls/skirts_c90317776', 'https://shop.mango.com/my/girls/underwear-and-pyjamas_c21080502', 'https://shop.mango.com/my/girls/shoes_c72445239', 'https://shop.mango.com/my/girls/scarves-and-hats_c19660561', 'https://shop.mango.com/my/girls/belts_c82604542', 'https://shop.mango.com/my/girls/bags_c11542942', 'https://shop.mango.com/my/girls/jewellery_c14884952', 'https://shop.mango.com/my/girls/more-accessories_c17719199']
    print(len(all_women_category))

    urls = scroll_each_url(all_women_category)

    # Remove the URL that has already been scraped to avoid duplication
    with open("Mango_Data.json", "r") as file:
        data = json.load(file)

    temp_list = []
    for each in data:
        temp_list.append(each["URL"])

    already_in_list = []
    for each in temp_list:
        # each = re.findall(r'[\S]+.html', each)[0]
        already_in_list.append(each)

    print("len of already_in_list", len(already_in_list))

    print("before remove: ", len(urls))
    for each in urls:
        urls.remove(each)
    print("after remove: ", len(urls))

    final_output = scrape_all(urls)

    write_to_file(final_output)

    end = time.time()
    time_taken = (end - start) / 60  # in minute
    print("Time taken: ", time_taken, " minutes")

    notification.notify(
        title='Meow~',
        message='Scraping All Done Master!',
        app_icon=r'C:\Users\User\Downloads\cat.ico',
        timeout=20,  # seconds
    )