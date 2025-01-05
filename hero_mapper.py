import json

# Load the JSON file
with open("HeroData.json", "r") as file:
    file_data = json.load(file)

# Initialize the dictionary to hold hero ID and name mappings
hero_id_name_map = {}

# Iterate through the list of heroes and build the dictionary
for hero in file_data:
    hero_id_name_map[hero["heroId"]] = hero["heroName"]

# Save the dictionary to a new JSON file
with open("heroDictionary.json", "w") as output_file:
    json.dump(hero_id_name_map, output_file, indent=4)

print("heroDictionary.json has been created.")
