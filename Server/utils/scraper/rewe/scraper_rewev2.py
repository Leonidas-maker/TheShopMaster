import sys
from requests import JSONDecodeError, ConnectionError, ConnectTimeout
import cloudscraper
from connector import main_db_connector 

# Regex for ammount (.*?)\s(\d+\sStück|\d+(,\d*)l|\d+ml|\d+g|\d+mg)
def scraper(marketIDs: list()):
    scraper = cloudscraper.create_scraper()
    for marketID in marketIDs:
        page = 1
        pages = 2
        productsList = []
        while page < pages + 1: 
            url = f"https://shop.rewe.de/api/products?&market={marketID}&\
                    objectsPerPage=100&page={page}&serviceTypes=PICKUP&sorting=RELEVANCE_DESC&source"
            try:
                data = scraper.get(url).json()
                if data.get("error"):
                    print("Error")
                    break
            except (JSONDecodeError, ConnectionError, ConnectTimeout):
                print("Error")
                break
            if pages == 2:
                pages = int(data["pagination"]["totalPages"])
            print(f"{page}/{pages}")

            products = data["_embedded"]["products"]
            
            for product in products:
                productTags = product["attributes"].get("tags", [])
                productInformation = product["_embedded"]["articles"][0]
                productPrice = productInformation["_embedded"]["listing"]["pricing"]

                productName = product["productName"].replace('"', "'")
                productEAN = productInformation["gtin"].rjust(16, "0")
                productImage = product["media"]["images"][0]["_links"]["self"]["href"]
                productVendor = product["brand"]["name"]
                productBasePrice = productPrice.get("basePrice")
                
                productBaseUnit_raw = productPrice.get("baseUnit")

                if productBaseUnit_raw:
                    tmp = list(productBaseUnit_raw.keys())
                    productBaseUnit = str(productBaseUnit_raw[tmp[0]]) + tmp[0]
                else:
                    productBaseUnit = "n/a"
                
                if "discounted" in productTags: 
                    productCurrentPrice = productPrice["currentRetailPrice"]
                    productRegularPrice = productPrice["discount"]["regularPrice"]
                    productDiscountedUntil = productPrice["discount"]["validTo"]
                    productHasDiscount = True
                else:
                    productCurrentPrice = productPrice["currentRetailPrice"]
                    productRegularPrice = productCurrentPrice
                    productDiscountedUntil = "n/a"
                    productHasDiscount = False

                productCategory = product["_embedded"]["categoryPath"]
                productsList.append((productEAN, productCategory, productName, productCurrentPrice, productRegularPrice, productHasDiscount, productDiscountedUntil, productBasePrice, productBaseUnit, productVendor, productImage))
                
            page += 1
        
        __database__.buildExecuteQuerry("rewe", productsList)

if __name__ == "__main__":
    __database__ = main_db_connector()
    __database__.connectDB()
    scraper([840145])
    __database__.commitAndClose()
