import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Set up logging
log_file = "stock_analysis.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("=== Script Execution Started ===")

# Define URL for fetching live data
url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"

# Headers to bypass bot protection
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Referer": "https://www.nseindia.com/",
}

# Function to fetch data safely
def fetch_data(url, headers):
    session = requests.Session()
    try:
        logging.info("Sending request to NSE website to fetch data.")
        session.get("https://www.nseindia.com", headers=headers, timeout=10)  # Initial request to get cookies
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an error for HTTP errors (e.g., 404, 500)
        logging.info("Data successfully fetched from NSE API.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None

# Fetch data
data = fetch_data(url, headers)
if not data or "data" not in data:
    logging.error("Error: No valid stock data received. Exiting.")
    exit()

# Convert JSON data to DataFrame
df = pd.DataFrame(data["data"])
logging.info(f"Successfully converted JSON data to DataFrame with {df.shape[0]} rows.")

# Clean column names
df.columns = df.columns.str.replace(r"\s+|\n", " ", regex=True).str.strip()

# Rename columns
column_mapping = {
    "symbol": "SYMBOL",
    "lastPrice": "LTP",
    "pChange": "%CHNG",
    "yearHigh": "52W H",
    "yearLow": "52W L",
    "perChange30d": "30 D %CHNG"
}

df.rename(columns=column_mapping, inplace=True)
logging.info("Renamed columns successfully.")

# Check if required columns exist
required_columns = ["SYMBOL", "LTP", "%CHNG", "52W H", "52W L", "30 D %CHNG"]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    logging.error(f"Error: Missing columns in data - {missing_columns}. Exiting.")
    exit()

# Convert numeric columns safely
numeric_columns = ["LTP", "%CHNG", "52W H", "52W L", "30 D %CHNG"]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')  # Converts, sets invalids to NaN

df.dropna(subset=numeric_columns, inplace=True)  # Drop rows where conversion failed
logging.info("Converted numeric columns and handled missing values.")

# Function to get top and bottom 5 stocks safely
def get_top(df, column):
    if column in df.columns:
        logging.info(f"Fetching top 5 stocks by {column}.")
        return df.nlargest(5, column)[["SYMBOL", column]]
    else:
        logging.warning(f"Column '{column}' not found in DataFrame.")
        return pd.DataFrame()

def get_bottom(df, column):
    if column in df.columns:
        logging.info(f"Fetching bottom 5 stocks by {column}.")
        return df.nsmallest(5, column)[["SYMBOL", column]]
    else:
        logging.warning(f"Column '{column}' not found in DataFrame.")
        return pd.DataFrame()

# Get gainers and losers
top_5_gainers = get_top(df, "%CHNG")
top_5_losers = get_bottom(df, "%CHNG")

logging.info("Top 5 Gainers:\n" + top_5_gainers.to_string(index=False))
logging.info("Top 5 Losers:\n" + top_5_losers.to_string(index=False))

# Plot gainers and losers
fig, ax = plt.subplots(1, 2, figsize=(14, 5))

if not top_5_gainers.empty:
    sns.barplot(x="SYMBOL", y="%CHNG", data=top_5_gainers, ax=ax[0], palette="Greens_r")
    ax[0].set_title("Top 5 Gainers")
    ax[0].set_ylabel("% Change")
    ax[0].set_xlabel("Stock Symbol")
    ax[0].tick_params(axis='x', rotation=45)

if not top_5_losers.empty:
    sns.barplot(x="SYMBOL", y="%CHNG", data=top_5_losers, ax=ax[1], palette="Reds_r")
    ax[1].set_title("Top 5 Losers")
    ax[1].set_ylabel("% Change")
    ax[1].set_xlabel("Stock Symbol")
    ax[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig("gainers_losers_chart.png")
plt.show()
logging.info("Saved gainers and losers chart as 'gainers_losers_chart.png'.")

# Get top 5 in last 30 days
top_5_in_last_30_days = get_top(df, "30 D %CHNG")
logging.info("Top 5 Stocks in Last 30 Days:\n" + top_5_in_last_30_days.to_string(index=False))

# Function to get stocks that are 30% below their 52-week high
def stocks_below_30_percent_high(df):
    if "LTP" in df.columns and "52W H" in df.columns:
        filtered_df = df[df["LTP"] <= 0.7 * df["52W H"]]
        return filtered_df[["SYMBOL", "LTP", "52W H"]]
    else:
        logging.warning("Warning: 'LTP' or '52W H' column not found in DataFrame.")
        return pd.DataFrame()

# Function to get stocks that are 20% above their 52-week low
def stocks_above_20_percent_low(df):
    if "LTP" in df.columns and "52W L" in df.columns:
        filtered_df = df[df["LTP"] >= 1.2 * df["52W L"]]
        return filtered_df[["SYMBOL", "LTP", "52W L"]]
    else:
        logging.warning("Warning: 'LTP' or '52W L' column not found in DataFrame.")
        return pd.DataFrame()

# Get filtered stocks
stocks_30_below_high = stocks_below_30_percent_high(df)
stocks_20_above_low = stocks_above_20_percent_low(df)

logging.info("\nStocks 30% below 52W High:\n" + stocks_30_below_high.to_string(index=False))
logging.info("\nStocks 20% above 52W Low:\n" + stocks_20_above_low.to_string(index=False))

logging.info("=== Script Execution Completed ===")
