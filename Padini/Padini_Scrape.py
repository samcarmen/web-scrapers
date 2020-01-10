from bs4 import BeautifulSoup as BS
import datetime
import json
import re
import requests


def get_image(soup):
    try:
        image = soup.find(class_="cloud-zoom product-image-gallery").get('href')
        return image
    except (TypeError, AttributeError, IndexError):
        print("Error retrieving image")


def get_brand(soup):
    try:
        brand = soup.find(class_="brand-name").text.strip('\n').strip('\t')
        return brand
    except (TypeError, AttributeError, IndexError):
        print("Error retrieving brand")


def get_product_code(soup):
    try:
        product_code = soup.find(class_="value").text
        return product_code
    except (TypeError, AttributeError, IndexError):
        print("Error retrieving product code")


def get_description(soup):
    try:
        description = soup.find(class_="short-description")
        description = description.find(class_='std').text.split('. ')
        return [each for each in description if each]
    except (TypeError, AttributeError, IndexError):
        print("Error retrieving description")


def get_colour(soup):
    try:
        colour = soup.find(class_="swatch-label")
        colour = colour.find('img').get('alt')
        return colour
    except (TypeError, AttributeError, IndexError):
        print("Error retrieving colour")


def get_sales_price(soup):
    try:
        price_container = soup.find(class_="price-box")
        reg_price = price_container.find(class_="regular-price")
        if reg_price is None:
            new_price = price_container.find(class_="special-price").find(class_="price").text.strip('\n')
            old_price = price_container.find(class_="old-price").find(class_="price").text.strip('\n')
            new_price = re.findall(r'\d+.\d+', new_price)[0]
            old_price = re.findall(r'\d+.\d+', old_price)[0]
            return new_price, old_price
        else:
            reg_price = reg_price.find(class_="price").text.strip('\n')
            reg_price = re.findall(r'\d+.\d+', reg_price)[0]
            return reg_price, reg_price
    except (TypeError, AttributeError, IndexError):
        print("Error retrieving price")
        return [None, None]


def get_name(soup):
    try:
        name = soup.find(class_="product-name").text.strip('\n')
        return name
    except (TypeError, AttributeError, IndexError):
        print("Error retrieving name")


def get_details(soup):
    try:
        det = soup.find(class_="panel")
        p = det.findAll('p')
        details = []
        for each in p:
            for b in each.findAll('b'):
                details.append("{}: {}".format(b.text.strip(':'), [br.nextSibling for br in each.findAll('br')]))
        return details
    except (TypeError, AttributeError, IndexError):
        print("Error retrieving details")


def get_category(soup):
    try:
        cat = soup.find(class_="breadcrumbs")
        each_cat = cat.findAll('li')
        real_cat = [each.find('span').text for each in each_cat]

        return real_cat
    except (TypeError, AttributeError, IndexError):
        print("Error retrieving category")


def get_mainlink(url):
    page = requests.get(url)
    soup = BS(page.content, 'lxml')

    main_cat = ["nav-item level0 nav-2 level-top nav-item--parent mega nav-item--only-subcategories parent",
                "nav-item level0 nav-3 level-top nav-item--parent mega nav-item--only-subcategories parent",
                "nav-item level0 nav-4 level-top nav-item--parent mega nav-item--only-subcategories parent",
                "nav-item level0 nav-5 level-top nav-item--parent mega nav-item--only-subcategories parent",
                "nav-item level0 nav-6 level-top nav-item--parent mega nav-item--only-subcategories parent",
                "nav-item level0 nav-7 level-top nav-item--parent mega nav-item--only-subcategories parent"]
    links_list = []

    for each in main_cat:
        print(each)
        try:
            links = soup.find(class_=each)
            links_temp = [each.get('href') for each in links.findAll('a')]
            for link in links_temp:
                links_list.append(link)
        except (TypeError, AttributeError, IndexError):
            continue

    print("Total number of links: ", len(links_list))
    for each in links_list:
        print(each)
    return links_list


def get_product(url):
    item_links = []
    for each in url:
        print("Processing: ", each)
        page = requests.get(each)
        soup = BS(page.content, 'lxml')
        category = get_category(soup)
        item = soup.findAll(class_="product-name")
        if item is None:
            continue
        all_links = [(each.find('a').get('href'), category) for each in item]
        for link in all_links:
            item_links.append(link)

        next_page = soup.find(class_="next ic ic-right")
        while next_page:
            next_link = next_page.get('href')
            print("Processing: ", next_link)
            page = requests.get(next_link)
            soup = BS(page.content, 'lxml')
            item = soup.findAll(class_="product-name")
            all_links = [(each.find('a').get('href'), category) for each in item]
            for link in all_links:
                item_links.append(link)
            next_page = soup.find(class_="next ic ic-right")

    item_links = [ele for ele in reversed(item_links)]

    print("Length before remove: ", len(item_links))
    seen = set()
    output = [(a, b) for a, b in item_links
              if not (a in seen or seen.add(a))]

    with open('Padini_Data.json', 'r') as outfile:
        data = json.load(outfile)

    done_url = [each['URL'] for each in data]
    output = [each for each in output if each[0] not in done_url]
    return output


def scrape(url):
    overall = []

    print("Total number of urls: ", len(url))

    for i in range(len(url)):
        current = url[i][0]

        print("Currently Processing: ", i+1, current)
        page = requests.get(current)
        soup = BS(page.content, 'lxml')

        if soup.find(class_="page-head-alt") is not None:
            print("Product cannot be found")
            continue

        image = get_image(soup)
        brand = get_brand(soup)
        product_code = get_product_code(soup)
        description = get_description(soup)
        price = get_sales_price(soup)
        colour = get_colour(soup)
        name = get_name(soup)
        details = get_details(soup)
        category = url[i][1]

        output = {
            "IMAGE": image,
            "BRAND": brand,
            "PRODUCT_CODE": product_code,
            "URL": current,
            "DESCRIPTION": description,
            "ORIGINAL_PRICE": {
                "PRICE": price[1],
                "CURRENCY": "RM"
            },
            "SALES_PRICE": {
                "PRICE": price[0],
                "CURRENCY": "RM"
            },
            "DETAILS": details,
            "CATEGORY": category,
            "COLOUR": colour,
            "NAME": name
        }

        overall.append(output)

    write_to_file(overall)


def write_to_file(output):
    with open('raw_scrape_padini.json', 'w') as outfile:
        json.dump(output, outfile)

    with open("raw_scrape_padini.json.", 'r') as json_file:
        parsed = json.load(json_file)

    pretty_output = json.dumps(parsed, indent=2)
    print(pretty_output)

    f = open("Padini_Data_Temp.json", "w")
    f.write(pretty_output)
    f.close()


if __name__ == "__main__":
    START = datetime.datetime.now()
    print("Start time: ", START)

    main = "https://www.padini.com/"
    super_links = get_mainlink(main)
    all_product = get_product(super_links)
    scrape(all_product)

    END = datetime.datetime.now()

    print("End time: ", START)

    total = END - START

    print("Total time taken: ", int(total.total_seconds() / 60))


"""
9.1.2020
18332 @ 12.48

10.1.2020
End time:  2020-01-09 12:48:49.614885
Total time taken:  1281
"""