from pctheory import array, group, pcseg, pcset, pitch, set_complex, tables, tempo, transformations, util
from fractions import Fraction
import json
import importlib.resources

json_data = None
with importlib.resources.open_text("pctheory", "abstract_subset24.json") as table_json:
    json_data = json.loads(table_json.read())

table = json_data["setClasses24"]
table.sort()
table = sorted(table, key=lambda x: len(x))

with open("pctheory/abstract_subset24_sorted.json", "w") as table_json:
    json_data = json.dumps(table)
    table_json.write(json_data)


