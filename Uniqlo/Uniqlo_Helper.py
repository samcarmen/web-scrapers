import json
from bs4 import BeautifulSoup as BS
import requests
import time

def remove_duplicate():
    with open('Uniqlo_Data.json', 'r') as file:
        data = json.load(file)

    unique = {each['PRODUCT_CODE']: each for each in data}.values()
    unique = [each for each in unique]
    print(len(data))
    print(len(unique))


def check_colour_correctness():
    with open('Uniqlo_Data.json', 'r') as file:
        data = json.load(file)

    colour_url = [[each['NAME'], each['COLOUR'], "http:"+each['IMAGE'], each['URL']] for each in data]
    for i in range(len(colour_url)):
        print(i)
        print(colour_url[i][0])
        print(colour_url[i][1])
        print(colour_url[i][2])
        print(colour_url[i][3])


def remove_home():
    with open('Uniqlo_Data.json', 'r') as file:
        data = json.load(file)

    for i in range(len(data)):
        category = data[i]['CATEGORY']
        data[i]['CATEGORY'] = [each for each in category if each != 'Home']

    pretty = json.dumps(data, indent=3)
    with open('Uniqlo_Data.json', 'w') as file:
        file.write(pretty)

remove_home()




