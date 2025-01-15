import os
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import zipfile
import io

# Set up Selenium WebDriver
chrome_driver_path = '/mnt/d/Code/Webdev/everygame/chromedriver'  # Update with the correct path to your ChromeDriver
chrome_binary_path = '/usr/bin/google-chrome'  # Path to the Chrome binary
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
options.binary_location = chrome_binary_path  # Specify the path to the Chrome binary
driver = webdriver.Chrome(service=service, options=options)

# URL to scrape
url = 'https://js13kgames.com/2018/games'

# Fetch the main page content
driver.get(url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'm-g')))

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Find all game links
main_div = soup.find('main', class_='m m-g index l-c')
if not main_div:
    print("Failed to find the main div.")
    exit()

game_links = main_div.find_all('a')

games_metadata = []

for link in game_links:
    game_url = "https://js13kgames.com/2018/" + link['href']

    game_id = game_url.split('/')[-1]
    game_title = link.find('h2').text.strip()
    
    # Fetch the game page content
    game_response = requests.get(game_url)
    game_soup = BeautifulSoup(game_response.content, 'html.parser')
    
    # Extract game instructions
    instructions_section = game_soup.find('section', id='m-g-v-desc')
    instructions = instructions_section.find('p').text.strip() if instructions_section else 'No instructions available'
    
    # Extract image source with class 'm-g-v-img-backdrop'
    img_tag = game_soup.find('img', class_='m-g-v-img-backdrop')
    img_src = img_tag['src'] if img_tag else 'No image available'
    
    # Ensure the image URL is absolute
    if img_src and not img_src.startswith('http'):
        img_src = 'https://js13kgames.com' + img_src
    
    # Extract the zip file URL
    zip_url = game_url + ".zip"
    
    print(zip_url)
    
    # Create folder and download/extract the zip file
    folder_path = f'./games_data/{game_id}'
    os.makedirs(folder_path, exist_ok=True)
    
    if zip_url:
        # Follow the redirection manually
        with requests.get(zip_url, stream=True) as r:
            r.raise_for_status()
            with open(f"{folder_path}/{game_id}.zip", 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        # Extract the zip file
        with zipfile.ZipFile(f"{folder_path}/{game_id}.zip", 'r') as zip_ref:
            zip_ref.extractall(folder_path)
    
    # Add game metadata to the list
    game_metadata = {
        "id": game_id,
        "title": game_title,
        "category": "Skill", 
        "subcategory": "Aiming",
        "instructions": instructions,
        "path": folder_path,
        "imgpath": img_src,
        "data_players": "120k",
        "related": ["vex7", "drive-mad", "moto-x3m"]
    }
    
    games_metadata.append(game_metadata)

# Save metadata to JSON file
with open('games_metadata.json', 'w', encoding='utf-8') as json_file:
    json.dump(games_metadata, json_file, indent=4)

print("Scraping completed and metadata saved to games_metadata.json")