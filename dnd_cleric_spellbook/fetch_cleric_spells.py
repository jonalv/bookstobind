import requests
import sys
import json

def fetch_cleric_spells(output_filename):
    # API endpoint for spells
    api_url = "https://www.dnd5eapi.co/api/spells/"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        spells = response.json()["results"]
        cleric_spells = []

        for spell in spells:
            spell_detail_response = requests.get(f"{api_url}{spell['index']}")
            if spell_detail_response.status_code == 200:
                spell_detail = spell_detail_response.json()
                if "Cleric" in spell_detail.get("classes", [{}])[0].get("name", ""):
                    cleric_spells.append(spell_detail)

        with open(output_filename, "w") as file:
            json.dump(cleric_spells, file, indent=4)
            
    else:
        print("Failed to fetch spells from API")

if __name__ == "__main__":
    output_filename = sys.argv[1]
    fetch_cleric_spells(output_filename)

