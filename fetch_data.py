import requests
import json

API_KEY = "94a8445b81f7409c8316095273c5c449"
URL = "https://newsapi.org/v2/top-headlines"

def fetch_data():
    params = {
        "country": "us",
        "apiKey": API_KEY
    }

    response = requests.get(URL, params=params)

    if response.status_code == 200:
        data = response.json()
        
        with open("data/raw_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        
        print("✅ Data fetched and saved to data/raw_data.json")
    else:
        print("❌ Failed to fetch data:", response.status_code)

if __name__ == "__main__":
    fetch_data()
