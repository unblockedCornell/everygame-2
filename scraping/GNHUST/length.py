import json

with open('/mnt/d/Code/Webdev/everygame/metadata/scraped_games.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Count the number of entries
num_entries = len(data)
print(f'The JSON file contains {num_entries} entries.')