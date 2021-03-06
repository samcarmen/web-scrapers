import json
import re


def process_duplicate():
    with open('Mango_Data_2.json') as file:
        parsed = json.load(file)

    unique = {each['IMAGE']: each for each in parsed}.values()
    unique = [each for each in unique]

    print("Original length:", len(parsed))
    print("Without duplicate: ", len(unique))
    print("Number of duplicate: ", len(parsed) - len(unique))

    with open('raw_scrape_mango.json', 'w') as outfile:
        json.dump(unique, outfile)

    with open("raw_scrape_mango.json", 'r') as json_file:
        parsed = json.load(json_file)

    pretty_output = json.dumps(parsed, indent=2)
    print(pretty_output)
    print(len(parsed))

    f = open("Mango_Data_2.json", "w")
    f.write(pretty_output)
    f.close()


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

    complete_list = [each for each in temp_parsed if each['IMAGE'] is not None]
    not_complete_list = [each['URL'] for each in temp_parsed if each['IMAGE'] is None]

    print("after remove empty:", len(complete_list))

    pretty_output = json.dumps(complete_list, indent=2)

    f = open("Mango_Data_Temp.json", "w")
    f.write(pretty_output)
    f.close()

    print(len(not_complete_list), not_complete_list)


def find_duplicate_url():
    with open("Mango_Data_Temp.json", "r") as file:
        data = json.load(file)

    already_in_list = []
    for each in data:
        already_in_list.append(each["URL"])

    for each in already_in_list:
        each = re.findall(r'[\S]+.html', each)[0]

    print(already_in_list)


def process_raw_scrape():
    with open("raw_scrape_mango.json", 'r') as json_file:
        parsed = json.load(json_file)

    pretty_output = json.dumps(parsed, indent=2)
    print(pretty_output)
    print(len(parsed))

    f = open("Mango_Data_Temp.json", "w")
    f.write(pretty_output)
    f.close()


# find_unsuccessful_scrape()
process_duplicate()
# process_raw_scrape()



