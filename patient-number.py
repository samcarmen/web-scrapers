with open("MRN.txt", 'r') as file:
    data = file.read().split('\n')

print("Before remove:", len(data))
print("After remove:", len(set(data)))

