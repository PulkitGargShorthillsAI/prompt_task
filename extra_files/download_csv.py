import requests
import pandas as pd

# Define URL
url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"

# Headers to bypass bot protection
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Referer": "https://www.nseindia.com/",
}

# Start session
session = requests.Session()
session.get("https://www.nseindia.com", headers=headers)  # Initial request to get cookies

# Fetch API data
response = session.get(url, headers=headers)
data = response.json()

# Extract stock details
stocks = data["data"]
df = pd.DataFrame(stocks)

# Save to CSV
df.to_csv("nifty_50_stocks.csv", index=False)
print("CSV file saved successfully!")



