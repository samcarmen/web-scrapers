import json
import re

from plyer import notification


def process_duplicate():
    with open('Mango_Data.json') as file:
        parsed = json.load(file)

    unique = {each['IMAGE']: each for each in parsed}.values()
    unique = [each for each in unique]

    print("With duplicate: ", len(parsed))
    print("Without duplicate: ", len(unique))

    # with open('raw_scrape_mango.json', 'w') as outfile:
    #     json.dump(unique, outfile)
    #
    # with open("raw_scrape_mango.json", 'r') as json_file:
    #     parsed = json.load(json_file)
    #
    # pretty_output = json.dumps(parsed, indent=2)
    # print(pretty_output)
    # print(len(parsed))
    #
    # f = open("Mango_Data_Temp.json", "w")
    # f.write(pretty_output)
    # f.close()


def find_unsuccessful_scrape():
    """
    Function to ensure that image and product reference data is complete
    :return:
    """
    not_complete_list = []
    # with open("Mango_Data.json", "r") as file:
    #     parsed = json.load(file)
    # print("before", len(parsed))

    with open("Mango_Data_Temp.json", "r") as file:
        temp_parsed = json.load(file)

    print("before remove empty: ", len(temp_parsed))

    for each in temp_parsed:
        if each['IMAGE'] is None or each["PRODUCT_REFERENCE"] is None:
            not_complete_list.append(each['URL'])
            temp_parsed.remove(each)

    print("after remove empty:", len(temp_parsed))

    pretty_output = json.dumps(temp_parsed, indent=2)

    f = open("Mango_Data_Temp.json", "w")
    f.write(pretty_output)
    f.close()

    print(len(not_complete_list), not_complete_list)


def find_duplicate_url():
    with open("Mango_Data.json", "r") as file:
        data = json.load(file)

    already_in_list = []
    for each in data:
        already_in_list.append(each["URL"])

    for each in already_in_list:
        each = re.findall(r'[\S]+.html', each)[0]

    print(already_in_list)


# find_unsuccessful_scrape()
# process_duplicate()


