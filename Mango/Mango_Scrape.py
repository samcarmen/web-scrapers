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
    options.add_argument("--headless")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--incognito")
    options.add_argument("User-Agent:'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'")
    options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\Carmen\Downloads\chromedriver_win32\chromedriver.exe")

    return driver


def make_soup(driver, url):
    driver.get(url)
    time.sleep(0.7)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    return soup


def get_all_url(soup):
    cat_list = []
    cat_keyword = ["Filter by Clothing", "Filter by Accessories", "Filter by Girls", "Filter by Baby girls",
                   "Filter by Baby boys", "Filter by Newborn", "Filter by New now"]

    for each in cat_keyword:
        try:
            clothing_container = soup.find('nav', {"aria-label": each})
            container = clothing_container.findAll('a')
            urls = [each.get('href') for each in container]
            urls = ["https://shop.mango.com" + each for each in urls]
            for url in urls:
                cat_list.append(url)
        except AttributeError:
            continue

    return cat_list


def scroll_category(url_list):
    all_url = []
    driver = initialise_web_driver()

    for i in range(len(url_list)):
        print("Processing url", i + 1)
        url = url_list[i]
        driver.get(url)  # open a new page
        driver.maximize_window()
        time.sleep(2)

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

            # Get the urls of the item
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            found_url = soup.findAll('a', class_="aZ-72")
            found_url = [each.get('href') for each in found_url]
            found_url = ["https://shop.mango.com" + each for each in found_url]

            for each in found_url:
                all_url.append(each)
            print(len(all_url))

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    print("all_url: ", len(all_url))
    print("set_url: ", len(set(all_url)))

    driver.close()
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
    regex = r"([a-zA-Z]+)(\d+.\d*)"

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
        big_container = soup.find(class_="product-info-block")
        container = big_container.findAll(class_="product-info-text")
        description = container[0].text.split('. ')
        description = [each.rstrip('.') for each in description]

        for each in container[1:]:
            if each.text != "":
                description.append(each.text.rstrip('.'))

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
            return image_url[0]
        except (TypeError, AttributeError, IndexError):
            print("*Error retrieving image")


def get_product_reference(soup):
    try:
        ref = soup.find(class_="product-reference").text
        return ref
    except (TypeError, AttributeError, IndexError):
        print("*Error retrieving product reference")


def scrape_all(url_list):
    driver = initialise_web_driver()

    for i in range(len(url_list)):
        url = url_list[i]
        print("Now processing: ", i+1, url)

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

        with open('raw_scrape_mango.json', 'a') as outfile:
            json.dump(output, outfile)
            outfile.write(',\n')

    driver.quit()


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

    main_urls = ["https://shop.mango.com/my/plus-size/essential-prices_d81191919",
                 "https://shop.mango.com/my/women/sale_d26824251",
                 "https://shop.mango.com/my/women/new-collection_d15794524",
                 "https://shop.mango.com/my/girls/we-like-to-party_d81787270",
                 "https://shop.mango.com/my/girls/best-sellers_d22987556",
                 "https://shop.mango.com/my/women/leandra-x-mango_d60084927",
                 "https://shop.mango.com/my/women/essential-prices_d93266323",
                 "https://shop.mango.com/my/women/best-sellers_d12580714",
                 "https://shop.mango.com/my/men/new-collection_d19853948",
                 "https://shop.mango.com/my/men/leather-and-more_d99003324"
                 "https://shop.mango.com/my/women/new-now_d71927648",
                 "https://shop.mango.com/my/men/sale_d14922989",
                 "https://shop.mango.com/my/girls/sale_d51229122",
                 "https://shop.mango.com/my/boys/sale",
                 "https://shop.mango.com/my/plus-size/sale_d15542249",
                 "https://shop.mango.com/my/women/gift-guide_d17441703",
                 "https://shop.mango.com/my/women/coats_c67886633",
                 "https://shop.mango.com/my/men/coats_c32859776",
                 "https://shop.mango.com/my/girls/coats_c10792813",
                 "https://shop.mango.com/my/baby-girls/coats_c17607080",
                 "https://shop.mango.com/my/baby-girls/coats_d19035082",
                 "https://shop.mango.com/my/boys/coats_c15872207",
                 "https://shop.mango.com/my/baby-boys/coats_c26307252",
                 "https://shop.mango.com/my/plus-size/coats_c11960442",
                 "https://shop.mango.com/my/women/sale_d26824251",

                 ]

    main_driver = initialise_web_driver()

    for url in main_urls:
        print("Processing: ", url)
        main_soup = make_soup(main_driver, url)
        all_category = get_all_url(main_soup)

        print("Total number of category: ", len(all_category))

        urls = scroll_category(all_category)

        # Remove the URL that has already been scraped to avoid duplication
        with open("Mango_Data_2.json", "r") as file:
            data = json.load(file)

        already_in_list = []
        for each in data:
            shorter = each['URL'].split('&')
            already_in_list.append(shorter[0])

        final_list = []
        for each in urls:
            if each.split('&')[0] not in already_in_list:
                final_list.append(each)

        print("before remove: ", len(urls))
        print("after remove: ", len(final_list))


        scrape_all(final_list)

    end = time.time()
    time_taken = (end - start) / 60  # in minute
    print("Time taken: ", time_taken, " minutes")

    notification.notify(
        title='Meow~',
        message='Scraping All Done Master!',
        app_icon=r'C:\Users\Carmen\Downloads\cat.ico',
        timeout=10,  # seconds
    )
