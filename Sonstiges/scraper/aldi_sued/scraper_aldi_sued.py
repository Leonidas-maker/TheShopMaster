import mysql.connector
from bs4 import BeautifulSoup
import requests

# Establish a connection to the MariaDB database
connection = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
cursor = connection.cursor()

header = {
    "authority": "www.aldi-sued.de",
    "accept": "*/*",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "referer": "https://www.aldi-sued.de/de/produkte/produktsortiment/kuehlung-und-tiefkuehlkost.html",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}


categories = ["kuehlung-und-tiefkuehlkost", "nahrungsmittel", "brot-aufstrich-und-cerealien", "kaffee-und-tee", "wein-und-sekt/rotwein", "wein-und-sekt/rosewein", 
            "wein-und-sekt/weisswein", "wein-und-sekt/schaum-perlwein", "getraenke", "suessigkeiten-und-snacks", "drogerie-und-kosmetik", "baby-und-kind",
            "haushalt", "tierbedarf", "aldi-guthaben-und-geschenkkarten", "grillen"
] #! Eissorten,blumen fehlen
for category in categories:
    page = 0

    # This is a Fixpoint Algorithm that breaks all rules of Aldo-Sued and the Universe
    while True:
        print(f"Get Category:{category}->Page:{page}")
        url = f"https://www.aldi-sued.de/de/produkte/produktsortiment/{category}.onlyProduct.html?pageNumber={page}"
        html = requests.get(url).content

        # Create a BeautifulSoup object
        soup = BeautifulSoup(html, "html.parser")

        # Extract information
        productTitles_raw = soup.find_all(class_="product-title")
        if not productTitles_raw:
            break
        productPrices_raw = soup.find_all(class_="at-product-price_lbl")
        productSubtitles_raw = soup.find_all(class_="additional-product-info")
        productImages_raw = soup.find_all(class_="plp_product__img")
        productAldiSuedIDs_raw = soup.find_all(class_="at-allproductteaserbox_grpl")

        productTitles = []
        productPrices = []
        productSubtitles = []
        productImages = []
        productAldiSuedIDs = []

        for x in range(len(productTitles_raw)):
            if productTitles_raw[x] and productPrices_raw[x]:
                productTitles.append(productTitles_raw[x].text.strip())
                productPrices.append(productPrices_raw[x].text.strip().replace("€ ", "") + "€")
                productSubtitles.append(productSubtitles_raw[x].text.replace(" ", "").replace("\n", ""))

                helperTMP = productImages_raw[x].find(class_="at-product-images_img")
                if (helperTMP):
                    productImages.append(helperTMP["data-src"].strip())
                else:
                    productImages.append("n/a")
                productAldiSuedIDs.append(productAldiSuedIDs_raw[x]["data-productid"].strip())

        insert_query = f'INSERT IGNORE INTO aldi_sued (product_id, product_category, product_title, product_subtitle, product_price, product_image) VALUES '
        for x in range(len(productTitles)):
            insert_query += f'("{productAldiSuedIDs[x]}", "{category}", "{productTitles[x]}", "{productSubtitles[x]}", "{productPrices[x]}", "{productImages[x]}")'
            if x != len(productTitles) - 1:
                insert_query += ',\n'
            else:
                insert_query += ';'

        cursor.execute(insert_query)
        
        page += 1

connection.commit()
cursor.close()
connection.close()