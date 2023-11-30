import json
import requests
import datetime

# Get current date
today = datetime.date.today()

# Get current year, month and day
year = int(today.strftime("%Y"))
month = int(today.strftime("%m"))
day = int(today.strftime("%d"))

# Get current week
week = datetime.date(year, month, day).isocalendar().week

# Url to get the offers
url = f"https://www.penny.de/.rest/offers/{year}-{week}"

# Get the data
response =  requests.get(url)
data = json.loads(response.text)

# Get the length of the categories
lenCat = len(data[0]["categories"])

for categories in data[0]["categories"]:
    for offerTiles in categories["offerTiles"]:
        print(offerTiles.get("title"))