import json
with open('CottonOn_Data.json') as file:
    parsed = json.load(file)

unique = { each['PRODUCT_CODE'] : each for each in parsed }.values()
new_unique = []
print(len(unique))
print(len(parsed))
# for i in unique:
#     new_unique.append(i)
#
# with open('CottonOn_Raw_Data.json', 'w') as outfile:
#     json.dump(new_unique, outfile)
#
# with open("CottonOn_Raw_Data.json", 'r') as json_file:
#     parsed = json.load(json_file)
#
# pretty_output = json.dumps(parsed, indent=2)
# print(pretty_output)
#
# f = open("CottonOn_Data_Temp.json", "w")
# f.write(pretty_output)
# f.close()


"""
1047
816

1226
995

1247
1010

1827
1489
"""
