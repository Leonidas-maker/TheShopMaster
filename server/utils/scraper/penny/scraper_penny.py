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
        productName = article.get("title")
        if productName:
            productType = article.get("type")
            productPrice = article.get("price")
            productBasePrice = article.get("basePrice")
            productQuantity = article.get("quantity")
            productDiscountPercentage = article.get("discountPercentage")
            productDiscount = article.get("discount")
            productOriginalPrice = article.get("originalPrice")
            productOriginalPriceType = article.get("originalPriceType")
            product = (productName, productPrice, productBasePrice, productType, productQuantity, productDiscount, productDiscountPercentage, productOriginalPrice, productOriginalPriceType)  
            print(product)
