import sys
from requests import JSONDecodeError, ConnectionError, ConnectTimeout
import cloudscraper
import mysql.connector

 
url = "https://mobile-api.rewe.de/api/v3/all-offers?marketCode=840623"
scraper = cloudscraper.create_scraper()
try:
    data = scraper.get(url).json()
    if data.get("error"):
        sys.exit(1)
except (JSONDecodeError, ConnectionError, ConnectTimeout):
    sys.exit(1)

# data got retrieved successfully
except (KeyError, TypeError):  
    pass

# Establish a connection to the MariaDB database
connection = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
cursor = connection.cursor()

for category in data.get("categories"):
    if category.get("id") not in  ["payback", "topangebote"]:
        productCategory = category.get("title") 
        for products in category.get("offers"):
            productTitle = products.get("title")
            if productTitle:
                productSubtitle = products.get("subtitle")
                productImage = ",".join(products.get("images")) 
                productPrice = products.get("priceData").get("price")
                productRegularPrice = products.get("priceData").get("regularPrice")

                productDetails = products.get("detail")

                productSontigeInformation = productDetails.get("pitchIn")
                productNumber = ""
                productVendor = ""
                for productDetail in productDetails.get("contents"):
                    if productDetail.get("header") == "Produktdetails":
                        for detailTitles in productDetail.get("titles"):
                            if  "Art.-Nr.:" in detailTitles:
                                productNumber = detailTitles.replace("Art.-Nr.:", "").strip()
                            elif "Hersteller:" in detailTitles:
                                productVendor = detailTitles.replace("Hersteller:", "").strip()
                
                insert_query = """
                    INSERT IGNORE INTO rewe_new 
                    (product_category, product_title, product_subtitle, product_image, product_price, product_regularPrice, product_sontigeInformation, product_number, product_vendor) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    productCategory, productTitle, productSubtitle, productImage, productPrice,
                    productRegularPrice, productSontigeInformation, productNumber, productVendor
                )
                cursor.execute(insert_query, values)
                connection.commit()