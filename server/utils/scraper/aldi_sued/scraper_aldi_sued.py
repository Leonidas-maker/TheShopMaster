import mysql.connector
from bs4 import BeautifulSoup
import requests
from connector import main_db_connector 
    
def getProduct(category, productTitle_raw, productPrices_raw, productSubtitle_raw, productImages_raw, productAldiSuedIDs_raw):
    # Create product information list
    productInformations = []

    # Save product information to lists
    for x in range(len(productTitle_raw)):
        if productTitle_raw[x]:
            # Get product title
            productTitle = productTitle_raw[x].text.strip()

            # Get product price
            helperTMP = productPrices_raw[x].text.strip().replace("€ ", "") 
            if helperTMP:
                helperTMP += "€"
            else:
                helperTMP = "variabel"
            productPrice = helperTMP

            # Get product subtitle
            productSubtitle = productSubtitle_raw[x].text.replace(" ", "").replace("\n", "")

            # Get product images
            helperTMP = productImages_raw[x].find(class_="at-product-images_img")
            if (helperTMP):
                productImage = helperTMP["data-src"].strip()
            else:
                productImage = "n/a"
            
            # Get AldiSuedIDs
            productAldiSuedID = productAldiSuedIDs_raw[x]["data-productid"].strip()

            #! Check for discount
            productInformations.append((productAldiSuedID, category, productTitle, productPrice, "", False, "", productSubtitle, "", productImage))
    #--end--main

    # Create DB-Querry
    __database__.buildExecuteQuerry("aldi_sued", productInformations)
    

def scaper():
    # Header for Anti-Bot Protection
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

    # All product categories
    categories = [
        "kuehlung-und-tiefkuehlkost", "nahrungsmittel", "brot-aufstrich-und-cerealien", "kaffee-und-tee", "wein-und-sekt/rotwein", "wein-und-sekt/rosewein", 
        "wein-und-sekt/weisswein", "wein-und-sekt/schaum-perlwein", "getraenke", "suessigkeiten-und-snacks", "drogerie-und-kosmetik", "baby-und-kind",
        "haushalt", "tierbedarf", "aldi-guthaben-und-geschenkkarten", "grillen"
        ] #! Eissorten, Blumen missing

    for category in categories:
        page = 0
        # This is a Fixpoint Algorithm that breaks all rules of Aldi-Sued
        while True:
            print(f"Get Category:{category}->Page:{page}")

            # Get the html of the aldi-sued page
            url = f"https://www.aldi-sued.de/de/produkte/produktsortiment/{category}.onlyProduct.html?pageNumber={page}"
            html = requests.get(url).content

            # Create a BeautifulSoup object
            soup = BeautifulSoup(html, "html.parser")

            # Extract information 1
            productTitle_raw = soup.find_all(class_="product-title")
            # There are no more products to save
            if not productTitle_raw:
                break
            # Extract information 2
            productPrices_raw = soup.find_all(class_="at-product-price_lbl")
            productSubtitle_raw = soup.find_all(class_="additional-product-info")
            productImages_raw = soup.find_all(class_="plp_product__img")
            productAldiSuedIDs_raw = soup.find_all(class_="at-allproductteaserbox_grpl")
            
            getProduct(category, productTitle_raw, productPrices_raw, productSubtitle_raw, productImages_raw, productAldiSuedIDs_raw)
            page += 1
    #--end--categories

if __name__ == "__main__":
    global __database__
    __database__ = main_db_connector()
    __database__.connectDB()
    scaper()
    __database__.commitAndClose()