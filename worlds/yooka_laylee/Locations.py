import json
import os

with open(os.path.join(os.path.dirname(__file__), 'locations.json'), 'r') as file:
    location_table = json.loads(file.read())

lookup_id_to_name = {}
j = 0
for item in location_table:
    j = j + 1
    lookup_id_to_name[item["id"]] = item["name"]
print(j)

lookup_id_to_name[None] = "Game Complete"
lookup_name_to_id = {name: id for id, name in lookup_id_to_name.items()}