import json
import os

def extractIdScore(folderPath):
    counterId = []
    counteredId = []
    compatibleId = []
    incompatibleId = []

    counter_filepath = os.path.join(folderPath, "counter.json")
    compatibility_filepath = os.path.join(folderPath, "compatibility.json")
    with open(counter_filepath, "r") as f1, open(compatibility_filepath, "r") as f2:
        counters_data = json.load(f1)
        compatibility_data = json.load(f2)

    # Example: Iterating through sub_heroes
    counter_sub_heroes = counters_data['data']['records'][0]['data']['sub_hero']
    counter_sub_heroes_last = counters_data['data']['records'][0]['data']['sub_hero_last']
    for idx, hero in enumerate(counter_sub_heroes, start=1):
        counterId.append(hero['heroid'])
    for idx, hero in enumerate(counter_sub_heroes_last, start=1):
        counteredId.append(hero['heroid'])

    compatibility_sub_heroes = compatibility_data['data']['records'][0]['data']['sub_hero']
    compatibility_sub_heroes_last = compatibility_data['data']['records'][0]['data']['sub_hero_last']
    for idx, hero in enumerate(compatibility_sub_heroes, start=1):
        compatibleId.append(hero['heroid'])
    for idx, hero in enumerate(compatibility_sub_heroes_last, start=1):
        incompatibleId.append(hero['heroid'])

    return counterId, counteredId, compatibleId, incompatibleId

def main():
    baseFolder = "../data/hero_data"
    for hero_id in range(1,128):
        heroFolder = "hero_" + str(hero_id)
        folderPath = os.path.join(baseFolder, heroFolder)
        counterId, counteredId, compatibleId, incompatibleId = extractIdScore(folderPath)
        data = {
                "counter": [str(id) for id in counterId],
                "countered": [str(id) for id in counteredId],
                "compatible": [str(id) for id in compatibleId],
                "incompatible": [str(id) for id in incompatibleId],
            }
        
        file_path = os.path.join(folderPath, "extractedRelationID.json")
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Finish extracting {hero_id}")

if __name__ == "__main__":
    main()