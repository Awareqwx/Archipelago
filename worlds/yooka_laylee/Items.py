import json
import os

with open(os.path.join(os.path.dirname(__file__), 'items.json'), 'r') as file:
    item_table = json.loads(file.read())

lookup_name_to_item = {}
lookup_name_to_id = {}

for item in item_table:
    item_name = item["name"]
    lookup_name_to_item[item_name] = item
    lookup_name_to_id[item_name] = item["id"]

lookup_name_to_id["Victory"] = None