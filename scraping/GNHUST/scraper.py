import os
import json
import requests
from bs4 import BeautifulSoup
import random

BASE_URL = "https://gnhustgames.github.io/"
OUTPUT_DIR = "games_data"

# Create output directories if not exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_player_count():
    # Possible ranges for player counts in different categories (low to medium player counts)
    player_ranges = [
        (500, 5000),   # Small range (low player counts)
        (5000, 20000), # Medium range
        (20000, 100000) # Large range, but still reasonable
    ]
    
    # Randomly choose a range
    selected_range = random.choice(player_ranges)
    
    # Generate a player count within the chosen range
    player_count = random.randint(selected_range[0], selected_range[1])
    
    # Format the player count with 'k' for thousands
    return f"{player_count // 1000}k players"

# Function to scrape game data
def scrape_game_data(game_url, img_src="https://media.wired.com/photos/61f48f02d0e55ccbebd52d15/3:2/w_2400,h_1600,c_limit/Gear-Rant-Game-Family-Plans-1334436001.jpg"):


    response = requests.get(game_url)
    if response.status_code != 200:
        print(f"Failed to fetch {game_url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title
    title_tag = soup.find("title")
    title = title_tag.text.split("-")[0].strip() if title_tag else "Unknown Title"
    print(title)

    # Generate ID from title
    game_id = title.lower().replace(" ", "-").replace("?", "").replace(",", "")

    # Extract iframe source
    iframe = soup.find("iframe")
    iframe_src = iframe['src']
    print(iframe_src)


    info_div = soup.find('div', class_='infor-first')
    instructions = info_div.find('p').get_text()

    # Create simplified HTML
    game_html = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>{}</title>
        <style>
            body {{
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #000;
            }}
            iframe {{
                border: none;
            }}
            #btn_fullscreen {{
                position: fixed;
                top: 10px;
                right: 10px;
                background-color: #fff;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                z-index: 1000;
            }}
        </style>
    </head>
    <body>
        <div id="btn_fullscreen">Full Screen</div>
        <iframe src="{}" 
                id="gameCanvas" 
                style="width: 90%; height: 90%;"></iframe>
        <script>
            // Full-Screen Functionality
            const btnFullscreen = document.getElementById('btn_fullscreen');
            const gameCanvas = document.getElementById('gameCanvas');

            btnFullscreen.addEventListener('click', () => {{
                if (gameCanvas.requestFullscreen) {{
                    gameCanvas.requestFullscreen();
                }} else if (gameCanvas.webkitRequestFullscreen) {{ // Safari
                    gameCanvas.webkitRequestFullscreen();
                }} else if (gameCanvas.msRequestFullscreen) {{ // IE11
                    gameCanvas.msRequestFullscreen();
                }}
            }});
        </script>
    </body>
    </html>"""
    
    game_html = game_html.format(title, iframe_src)



    # Save HTML to file
    game_dir = os.path.join(OUTPUT_DIR, game_id)
    os.makedirs(game_dir, exist_ok=True)
    with open(os.path.join(game_dir, "index.html"), "w", encoding="utf-8") as file:
        file.write(game_html)

    return {
        "id": game_id,
        "title": title,
        "category":"Skill",
        "subcategory":"Aiming",
        "instructions": instructions,
        "path": f"scraping/GNHUST/games_data/{game_id}/",
        "imgpath":img_src,
        "data_players": generate_player_count(),
        "related":["drive-mad","retro-bowl","bob-the-robber-2"]
    }




def scrape_gameurls_and_images():
    # Read the local HTML file
    with open('/mnt/d/Code/Webdev/everygame/scraping/GNHUST/popular.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    print(soup)
    games = []

    for item in soup.select('#populargames .item'):
        a_tag = item.find('a')
        img_tag = item.find('img')
        if a_tag and img_tag:
            game_url = a_tag['href']
            img_src = img_tag['src']
            games.append((game_url, img_src))

    return games





# List of game URLs (replace with actual game links)

# game_urls = scrape_gameurls_and_images()

game_urls = scrape_gameurls_and_images()

# Metadata list
games_metadata = []

# Scrape data for each game
for url, imgsrc in game_urls:
    try:
        game_data = scrape_game_data(url, imgsrc)
        if game_data:
            games_metadata.append(game_data)
    except:
        pass

# Save metadata to JSON file
metadata_path = os.path.join(OUTPUT_DIR, "games_metadata.json")
with open(metadata_path, "w", encoding="utf-8") as json_file:
    json.dump(games_metadata, json_file, indent=4)

print(f"Scraping complete. Metadata saved to {metadata_path}")
