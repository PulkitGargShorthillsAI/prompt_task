import requests
import csv
import json

def scrape_nifty50_data(csv_filename="nifty50_data.csv"):
    """
    Scrapes NIFTY 50 stock data from NSE API and saves it to a CSV file.
    """
    url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/",
    }

    session = requests.Session()
    session.headers.update(headers)

    # Get session cookies from NSE homepage
    try:
        session.get("https://www.nseindia.com", timeout=5)
    except requests.RequestException as e:
        print(f"Error accessing NSE homepage: {e}")
        return

    # Fetch stock data from the API
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx

        data = response.json()  # Parse JSON response
        stock_data_list = data.get("data", [])

        if not stock_data_list:
            print("No stock data found in the response.")
            return

    except requests.RequestException as e:
        print(f"Error fetching data from NSE: {e}")
        return
    except json.JSONDecodeError:
        print("Failed to parse JSON response.")
        return

    # Define CSV headers
    csv_headers = [
        "symbol", "open", "dayHigh", "dayLow", "lastPrice", "previousClose",
        "change", "pChange", "totalTradedVolume", "totalTradedValue",
        "yearHigh", "yearLow","30DayChange "
    ]

    # Write data to CSV
    try:
        with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            writer.writeheader()

            for stock in stock_data_list:
                writer.writerow({key: stock.get(key, "") for key in csv_headers})

        print(f"Data successfully saved to {csv_filename}")

    except Exception as e:
        print(f"Error writing to CSV: {e}")

if __name__ == "__main__":
    scrape_nifty50_data("nifty50_data.csv")
