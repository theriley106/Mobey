import json
import sys

result = []
with open(sys.argv[1]) as json_data:
    data = json.load(json_data)
    for i in data:
        result.append([i['location']['latitude'], i['location']['longitude']])

print(result)