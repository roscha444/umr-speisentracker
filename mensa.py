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
foodResults = parsedContent.find_all("tr", attrs={"data-canteen":canteen})

todaysFood = []

for food in foodResults:
    foodName = food.find("span").text.strip()
    foodDate = datetime.strptime(food.attrs["data-date"], "%Y-%m-%d").date()
    if(today == foodDate):
        todaysFood.append(foodName)

if(len(todaysFood) > 0):
    discordMessage = "**"
    if(os.environ.get("CANTEEN")=="340"):
        discordMessage += "Mensa Lahnberge"
    elif(os.environ.get("CANTEEN")=="420"):
        discordMessage += "Mo's Diner"
    elif(os.environ.get("CANTEEN")=="490"):
        discordMessage += "Cafeteria Lahnberge"
    discordMessage += " am " + today.strftime("%d.%m.%Y") + "**\n\n"

    for food in todaysFood:
        food = re.sub(r"\([^()]*\)", "", food)
        discordMessage += food + "\n\n"

    requests.post(os.environ.get("API"), json={"content" : discordMessage})