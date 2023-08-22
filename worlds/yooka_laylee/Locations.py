import json
import pkgutil

location_table = json.loads(pkgutil.get_data(__name__, "locations.json").decode())

lookup_name_to_id = {}
priority_locations = []
for item in location_table:
    lookup_name_to_id[item["name"]] = item["id"]
    if "type" in item and item["type"] == "Priority":
        priority_locations.append(item["name"])

lookup_name_to_id["Game Complete"] = None