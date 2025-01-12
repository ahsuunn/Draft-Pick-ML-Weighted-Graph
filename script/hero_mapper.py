import json

with open("../data/HeroData.json", "r") as file:
    file_data = json.load(file)

hero_id_name_map = {}
for hero in file_data:
    hero_id_name_map[hero["heroId"]] = hero["heroName"]

with open("../data/heroDictionary.json", "w") as output_file:
    json.dump(hero_id_name_map, output_file, indent=4)

print("../data/heroDictionary.json has been created.")
