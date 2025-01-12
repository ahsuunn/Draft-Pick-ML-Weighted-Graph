import json
import os

def combineIdScore(folderPath):
    try:
        hero_filepath = os.path.join(folderPath, "hero.json")
        relation_filepath = os.path.join(folderPath, 'extractedRelationId.json')
        weight_filepath = os.path.join(folderPath, 'weight.json')
        with open(hero_filepath, "r") as f1, open(relation_filepath, 'r') as f2, open(weight_filepath, 'r') as f3:
            hero_data = json.load(f1)
            id = json.load(f2)
            weight = json.load(f3)

        # Extract relevant data
        heroName = hero_data['data']['records'][0]['data']['hero']['data']['name']
        heroId = hero_data['data']['records'][0]['data']['hero_id']

        # Combine the data from both JSONs into a new structure
        relation_data = {
            "counter": [
                {"hero_id": counter, "value": weight}
                for counter, weight in zip(id['counter'], weight['counter'])
            ],
            "countered": [
                {"hero_id": countered, "value": weight}
                for countered, weight in zip(id['countered'], weight['countered'])
            ],
            "compatible": [
                {"hero_id": compatible, "value": weight}
                for compatible, weight in zip(id['compatible'], weight['compatible'])
            ],
            "incompatible": [
                {"hero_id": incompatible, "value": weight}
                for incompatible, weight in zip(id['incompatible'], weight['incompatible'])
            ]
        }

        combinedHeroData = {
            "heroId" : heroId,
            "heroName" : heroName,
            "relationData" : relation_data,
        }

        return combinedHeroData

    except Exception as E:
        print(f"Error occured: {E}") 

def main():
    baseFolder = "../data/hero_data"
    finalData = []
    for hero_id in range(1,128):
        heroFolder = "hero_" + str(hero_id)
        folderPath = os.path.join(baseFolder, heroFolder)
        combineHeroData = combineIdScore(folderPath)
        finalData.append(combineHeroData)
        print(f"Finish Combining Hero ID {hero_id}")

    # Save the combined data to a new JSON file
    with open('../data/HeroData.json', 'w') as output_file:
        json.dump(finalData, output_file, indent=4)

if __name__ == "__main__":
    main()