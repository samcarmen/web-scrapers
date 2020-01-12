mytup = [("hi", [1, 2]), ("yo", [1]), ("hi", [1,2,3])]

visited = set()
seen = set()
output = []
for a, b in mytup:
    if not a in visited:
        visited.add(a)
        output.append((a, b))

print(output)
