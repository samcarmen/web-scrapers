import json


def write_to_file(output):
    with open('raw_scrape_padini.json', 'w') as outfile:
        json.dump(output, outfile)

    with open("raw_scrape_padini.json.", 'r') as json_file:
        parsed = json.load(json_file)

    pretty_output = json.dumps(parsed, indent=2)
    # print(pretty_output)

    f = open("Padini_Data_Temp.json", "w")
    f.write(pretty_output)
    f.close()


def find_null():
    not_complete_list = []
    # with open("Mango_Data.json", "r") as file:
    #     parsed = json.load(file)
    # print("before", len(parsed))

    with open("Padini_Data_Temp.json", "r") as file:
        temp_parsed = json.load(file)

    print("before remove empty: ", len(temp_parsed))

    complete_list = [each for each in temp_parsed if each['IMAGE'] is not None]
    not_complete_list = [(each['URL'], each['CATEGORY']) for each in temp_parsed if each['IMAGE'] is None]

    print("after remove empty:", len(complete_list))

    pretty_output = json.dumps(complete_list, indent=2)

    f = open("Padini_Data_Temp.json", "w")
    f.write(pretty_output)
    f.close()

    print(len(not_complete_list), not_complete_list)


def change_details():
    with open('Padini_Data_Temp.json', 'r') as file:
        data = json.load(file)

    for i in range(len(data)):
        try:
            details = data[i]['DETAILS']
            each = [each.split(':') for each in details]
            new = {indi[0]: eval(indi[1]) for indi in each}
            data[i]['DETAILS'] = new
        except:
            continue

    write_to_file(data)


def remove_duplicate():
    with open('Padini_Data.json', 'r') as file:
        data = json.load(file)
    print(len(data))
    not_unique = [each for each in data]
    unique = {each['IMAGE']: each for each in data}.values()
    unique = [each for each in unique]
    print("Before", len(unique))
    for not_uni in not_unique:
        for i in range(len(unique)):
            if not_uni['IMAGE'] == unique[i]['IMAGE'] and len(not_uni['CATEGORY']) > len(unique[i]['CATEGORY']):
                unique[i] = not_uni
            else:
                continue
    print(len(data))
    print("After", len(unique))

    write_to_file(unique)




