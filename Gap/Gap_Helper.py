def extract_info(link):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("User-Agent:'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'")
    driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\User\Downloads\chromedriver\chromedriver.exe")
    driver.get(link)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    print(soup)
    # page = requests.get(link)
    # soup = BeautifulSoup(page.content, 'lxml')
    try:
        name = soup.find(class_="product-title__text").text

        color = soup.find(class_="label-value").text

        price = soup.find(class_="pdp-pricing__selected pdp-pricing--highlight")

        container = soup.findAll(class_="product-information-item__list")
        details = container[0].findAll(class_="product-information-item__list-item")
        details[:] = [each.text.strip() for each in details]
        details[:] = [each.rstrip('.') for each in details]

        pattern = re.compile(r'#\d+')
        for each in details:
            product_code = re.findall(pattern, each)

        details[:] = [each for each in details if each not in product_code]

        care = container[1].findAll(class_="product-information-item__list-item")
        care[:] = [each.text for each in care]

        image = "https://www.gap.com" + str(soup.find(class_="product-photo--image image-visible").get('src'))

        category = (soup.find(class_="product-breadcrumb").findAll('a'))
        cat = [each.text for each in category]

        output = {
            "IMAGE": image,
            "BRAND": "Gap",
            "URL": link,
            "PRODUCT_CODE": product_code[0],
            "DETAILS": details,
            "PRICE": price,
            "FABRIC_CARE": care,
            "CATEGORY": cat,
            "COLOUR": color,
            "NAME": name
        }
        print(output)

    except Exception as e:
        print(e)


def get_mainLinks(homepage):
    print("Into function")
    pageLinks = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

    try:
        doc = html.fromstring(page.content)
        print(doc)
        XPATH_LINK = '//*[@id="app"]/div[2]/div/div[2]/div/div/a'

        RAW_LINKS = doc.xpath(XPATH_LINK)

        LINKS = ' '.join(RAW_LINKS).strip() if RAW_LINKS else None

        for url in LINKS.split():
            print(url)
            link = "https://www.gap.com" + url
            pageLinks.append(link)

    except Exception as e:
        print(e)

    return pageLinks


if __name__ == "__main__":
    # main_links = get_mainLinks(homepage="https://www.gap.com/")
    extract_info(
        "https://www.gap.com/browse/product.do?pid=519290012&cid=1148398&pcid=8792&vid=1&grid=pds_0_211_1#pdp-page-content")
