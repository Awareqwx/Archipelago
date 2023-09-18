import json
import pkgutil

item_table = json.loads(pkgutil.get_data(__name__, "items.json").decode())

lookup_name_to_item = {}
lookup_name_to_id = {}

for item in item_table:
    item_name = item["name"]
    lookup_name_to_item[item_name] = item
    lookup_name_to_id[item_name] = item["id"]

lookup_name_to_id["Victory"] = None