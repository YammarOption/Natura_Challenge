import os
import json

files = os.listdir("mons_json")

for file in files:
    prev_level=0
    found_something=False
    with open("mons_json/"+file, "r", encoding="utf-8") as f:
        data = json.load(f)
    for i  in data["level_up_moves"]:
        if i[0]==0:
            continue
        if i[0]==prev_level:
            print(f"found one in file {file}: level{i[0]}")
            found_something=True
        prev_level= i[0]
    if not found_something:
        print(f"File {file} is clean")
