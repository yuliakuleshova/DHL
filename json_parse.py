import sys
import json
import re

snapshots = str(sys.argv[1])

with open(snapshots, "r", encoding='utf-8') as json_file:
    snap_list = json.load(json_file)

new_data = []

for snap in snap_list['Snapshots']:
    s = snap['Description']
    if not re.match(r"Created for policy:", s):
        new_data.append(snap)

with open("output.txt", "w") as txt_file:
    for i in new_data:
        txt_file.write(" ".join(i) + "\n")