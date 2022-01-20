import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime
import re

load_dotenv()
canteen = os.environ.get("CANTEEN")
today = datetime.now().date()

url = os.environ.get("URL")
site = requests.get(url)
parsedContent = BeautifulSoup(site.content, "html.parser")
results = parsedContent.find_all("tr", attrs={"data-canteen":canteen})

todaysFood = []

for entry in results:
    food = entry.findAll("span")
    foodName = food[0].text.strip()
    if(food[2].text.strip() == "vegan"):
        foodName += " **vegan** "
        foodPrice = food[4].text.strip()
    else:
        foodPrice = food[2].text.strip()
    foodDate = datetime.strptime(entry.attrs["data-date"], "%Y-%m-%d").date()
    if(today == foodDate):
        todaysFood.append({"name":foodName, "price": foodPrice})

if(len(todaysFood) > 0):
    discordMessage = "**"
    if(os.environ.get("CANTEEN")=="340"):
        discordMessage += "Mensa Lahnberge"
    elif(os.environ.get("CANTEEN")=="420"):
        discordMessage += "Mo's Diner"
    elif(os.environ.get("CANTEEN")=="490"):
        discordMessage += "Cafeteria Lahnberge"
    discordMessage += " am " + today.strftime("%d.%m.%Y") + "**\n\n"

    for entry in todaysFood:
        name = re.sub(r"\([^()]*\)", "", entry["name"])
        discordMessage += name + " " + entry["price"] + "\n\n"

    requests.post(os.environ.get("API"), json={"content" : discordMessage})