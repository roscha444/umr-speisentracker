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

todaysMeals = []

for entry in results:
    mealDetails = entry.findAll("span")
    if(len(mealDetails) > 2):
        mealName = mealDetails[0].text.strip()
        if("€" in mealDetails[2].text.strip()):
            mealPrice = mealDetails[2].text.strip()
        else:
            mealName += "  **" + mealDetails[3].text.strip() + "**"
            mealPrice = mealDetails[4].text.strip()
        foodDate = datetime.strptime(entry.attrs["data-date"], "%Y-%m-%d").date()
        if(today < foodDate):
            mealName = re.sub(" \([^()]*\)( ){0,1}", "", mealName)
            meal = mealName + " " + mealPrice + "\n\n"
            todaysMeals.append(meal)

if(len(todaysMeals) > 0):
    discordMessage = "**"
    if(os.environ.get("CANTEEN")=="340"):
        discordMessage += "Mensa Lahnberge"
    elif(os.environ.get("CANTEEN")=="420"):
        discordMessage += "Mo's Diner"
    elif(os.environ.get("CANTEEN")=="490"):
        discordMessage += "Cafeteria Lahnberge"
    elif(os.environ.get("CANTEEN")=="330"):
        discordMessage += "Mensa Erlenring"
    elif(os.environ.get("CANTEEN")=="460"):
        discordMessage += "Bistro"
    
    discordMessage += " am " + today.strftime("%d.%m.%Y") + "**\n\n"

    for entry in todaysMeals:
        discordMessage += entry

    requests.post(os.environ.get("API"), json={"content" : discordMessage})