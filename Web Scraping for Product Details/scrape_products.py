import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse

headers = {"User-Agent": "Mozilla/5.0"}

def scrape_flipkart(search):
    products = []
    try:
        url = f"https://www.flipkart.com/search?q={urllib.parse.quote(search)}"
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        names = soup.find_all("div", class_="_4rR01T")
        prices = soup.find_all("div", class_="_30jeq3 _1_WHN1")
        ratings = soup.find_all("div", class_="_3LWZlK")

        for i in range(len(names)):
            products.append({
                "Site": "Flipkart",
                "Name": names[i].get_text(strip=True),
                "Price": prices[i].get_text(strip=True) if i < len(prices) else "N/A",
                "Rating": ratings[i].get_text(strip=True) if i < len(ratings) else "N/A"
            })
    except Exception as e:
        print(f"[Flipkart] Error: {e}")
    return products

def scrape_reliance(search):
    products = []
    try:
        url = f"https://www.reliancedigital.in/search?q={urllib.parse.quote(search)}"
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        names = soup.find_all("p", class_="sp__name")
        prices = soup.find_all("span", class_="sc-bxivhb finalPrice")

        for i in range(len(names)):
            products.append({
                "Site": "Reliance Digital",
                "Name": names[i].get_text(strip=True),
                "Price": prices[i].get_text(strip=True) if i < len(prices) else "N/A",
                "Rating": "N/A"
            })
    except Exception as e:
        print(f"[Reliance Digital] Error: {e}")
    return products

if __name__ == "__main__":
    search_item = input("Enter product to search: ").strip()
    if not search_item:
        print("Search term cannot be empty.")
        exit()

    data = []
    data.extend(scrape_flipkart(search_item))
    data.extend(scrape_reliance(search_item))

    if data:
        df = pd.DataFrame(data)
        df.to_excel("products.xlsx", index=False)
        print(f"✅ Data saved to products.xlsx ({len(data)} items)")
    else:
        print("⚠ No data found for your search.")
