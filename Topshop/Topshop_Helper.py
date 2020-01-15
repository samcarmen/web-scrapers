import json

import requests
from bs4 import BeautifulSoup


def openfile(filename):
    with open(filename, 'r') as file:
        parsed = json.load(file)
    return parsed


def get_unique():
    data = openfile('Topshop_Data.json')

    unique = set()
    unique_list = []

    for each in data:
        if each['PRODUCT_CODE'] not in unique:
            unique.add(each['PRODUCT_CODE'])
            unique_list.append(each)

    # unique = {each['PRODUCT_CODE']: each for each in data}.values()
    # unique = [each for each in unique]

    print("Before remove duplicate: ", len(data))
    print("After remove duplicate: ", len(unique_list))

    pretty = json.dumps(unique_list, indent=3)
    with open("Topshop_Data.json", 'w') as file:
        file.write(pretty)


def make_soup(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.117 Safari/537.36'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'lxml')
        return soup
    except (AttributeError, IndexError, TypeError):
        print("Error making soup")
        return None


def change_detail():
    data = openfile('Topshop_Data_Modified.json')

    complete = [each for each in data if each['PRODUCT_CODE'] is not None]
    not_complete = [each for each in data if each['PRODUCT_CODE'] is None]

    print(len(complete))
    print(len(not_complete))

    for i in range(len(not_complete)):
        current_data = not_complete[i]
        url = current_data['URL']
        print("Currently processing: ", i+1, url)
        soup = make_soup(url)
        try:
            name = soup.find(class_="Bundles-title").text
            not_complete[i]['NAME'] = name

            code_raw = soup.find(class_="ProductDescriptionExtras-item").text
            code = code_raw.split(': ')[1]
            not_complete[i]['PRODUCT_CODE'] = code
        except Exception as e:
            print(e, url)

    for each in not_complete:
        complete.append(each)

    pretty_data = json.dumps(complete, indent=3)

    with open("Topshop_Data.json", 'w') as file:
        file.write(pretty_data)


def change_care_instruction():
    data = openfile('Topshop_Data.json')

    for i in range(len(data)):
        current_data = data[i]
        details = current_data['DETAILS']

        if "Dry clean only" in details:
            details = [each for each in details if each != "Dry clean only"]
            current_data['CARE_INSTRUCTION'].append("Dry clean only")
            data[i]['DETAILS'] = details

    pretty_data = json.dumps(data, indent=3)

    with open("Topshop_Data.json", 'w') as file:
        file.write(pretty_data)


# get_unique()
# change_care_instruction()
"""
17B05SBLK
check if the longest list is taken
"""
