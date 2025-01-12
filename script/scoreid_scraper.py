import os
import requests
import json

base_url = "https://api.gms.moontontech.com/api/gms/source/2669606/"
score_url = "2756569"
hero_url = "2756564"
    
headers = {"Content-Type": "application/json"}

base_dir = "../data/hero_data"
os.makedirs(base_dir, exist_ok=True)

match_types = [
    {"value": 0, "filename": "counter.json"},       # Counter relationships
    {"value": 1, "filename": "compatibility.json"}, # Compatibility relationships
]

for hero_id in range(1, 128):
    hero_dir = os.path.join(base_dir, f"hero_{hero_id}")
    os.makedirs(hero_dir, exist_ok=True)
    hero_payload={"pageSize":20,
                       "filters":[
                           {"field":"hero_id","operator":"eq","value":str(hero_id)}
                           ],
                           "sorts":[],
                           "pageIndex":1,
                           "object":[]}

    for match_type in match_types:  
        score_payload = {
            "pageSize": 20,
            "filters": [
                {"field": "match_type", "operator": "eq", "value": str(match_type["value"])},
                {"field": "main_heroid", "operator": "eq", "value": str(hero_id)},
                {"field": "bigrank", "operator": "eq", "value": "7"}
            ],
            "sorts": [],
            "pageIndex": 1
        }

        try:
            response = requests.post(base_url+score_url, json=score_payload, headers=headers)
            response.raise_for_status()

            data = response.json()

            file_path = os.path.join(hero_dir, match_type["filename"])
            with open(file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for Hero ID {hero_id}, match type {match_type['value']}: {e}")


    try:
        response = requests.post(base_url+hero_url, json=hero_payload, headers=headers)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Save the data into a JSON file
        file_path = os.path.join(hero_dir, "hero.json")
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Saved data for Hero ID {hero_id}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for Hero ID {hero_id}, match type {match_type['value']}: {e}")

print("Data extraction complete.")
