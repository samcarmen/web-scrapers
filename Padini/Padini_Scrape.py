from bs4 import BeautifulSoup
import requests


def get_image(soup):
    try:
        image = soup.find(class_="cloud-zoom product-image-gallery").get('href')
        return image
    except Exception as e:
        print("Error retrieving image")


def get_brand(soup):
    try:
        brand = soup.find(class_="brand-name").text.strip('\n').strip('\t')
        return brand
    except:
        print("Error retrieving brand")


def get_product_code(soup):
    try:
        product_code = soup.find(class_="value").text
        return product_code
    except:
        print("Error retrieving product code")


def get_description(soup):
    try:
        description = soup.find(class_="short-description")
        description = description.find(class_='std').text.split('.')
        return description
    except:
        print("Error retrieving description")


def get_colour(soup):
    try:
        colour = soup.find(class_="swatch-label")
        colour = colour.find('img').get('alt')
        return description
    except:
        print("Error retrieving colour")


def get_price(soup):
    try:
        container = soup.find(class_="regular-price")
        price = [each.text for each in container.find(class_="class")]
        return price
    except:
        print("Error retrieving price")


def get_name(soup):
    try:
        name = soup.find(class_="product-name").text.strip('\n')
        return name
    except:
        print("Error retrieving name")


if __name__ == "__main__":
    url = "https://www.padini.com/women/brandsoutlet-disney-short-sleeve-logo-t-ladies-tee-BO20255727.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    image = get_image(soup)
    brand = get_brand(soup)
    product_code = get_product_code(soup)
    description = get_description(soup)
    price = get_price(soup)
    colour = get_colour(soup)
    name = get_name(soup)

    output = {
        "IMAGE": image,
        "BRAND": brand,
        "PRODUCT_CODE": product_code,
        "URL": url,
        "DESCRIPTION": description,
        "PRICE": price,
        "COLOUR": colour,
        "NAME": name
    }

    print(output)