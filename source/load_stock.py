import json

with open('../stock.json') as f:
    data = json.load(f)

print(type(data))
print(len(data))