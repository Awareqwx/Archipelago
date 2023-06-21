import json
import pkgutil

location_table = json.loads(pkgutil.get_data(__name__, "locations.json").decode())

lookup_name_to_id = {}
for item in location_table:
    lookup_name_to_id[item["name"]] = item["id"]

lookup_name_to_id["Game Complete"] = None