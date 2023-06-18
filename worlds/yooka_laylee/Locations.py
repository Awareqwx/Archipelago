import json
import os

with open(os.path.join(os.path.dirname(__file__), 'locations.json'), 'r') as file:
    location_table = json.loads(file.read())

lookup_name_to_id = {}
for item in location_table:
    lookup_name_to_id[item["name"]] = item["id"]

lookup_name_to_id["Game Complete"] = None