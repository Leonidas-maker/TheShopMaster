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

categories = data[0]["categories"]

#TODO productData need to be parsed
for category in categories:
    for article in category["offerTiles"]:
        product_name = article.get("title")
        if product_name:
            product_price = article.get("price")
            product_quantity = article.get("quantity")
            product_originalPrice = article.get("originalPrice")
            product_originalPriceType = article.get("originalPriceType")
            product =(product_name, product_price, product_quantity, product_originalPrice, product_originalPriceType)  
            print(product)
