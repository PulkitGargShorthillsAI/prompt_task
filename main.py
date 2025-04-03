import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define URL for fetching live data
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

# Convert JSON data to DataFrame
df = pd.DataFrame(data["data"])

# Clean column names
df.columns = df.columns.str.replace(r"\s+|\n", " ", regex=True).str.strip()

print(df)

# Rename columns to match your structure
df.rename(columns={
    "symbol": "SYMBOL",
    "lastPrice": "LTP",
    "pChange": "%CHNG",
    "yearHigh": "52W H",  # Placeholder for 52-week high (update if needed)
    "yearLow": "52W L",   # Placeholder for 52-week low (update if needed)
}, inplace=True)

# Convert numeric columns
numeric_columns = ["LTP", "%CHNG"]
for col in numeric_columns:
    df[col] = df[col].astype(str).str.replace(",", "").astype(float)

# Function to get top and bottom 5 stocks
def get_top(df, column):
    return df.nlargest(5, column)[["SYMBOL", column]]

def get_bottom(df, column):
    return df.nsmallest(5, column)[["SYMBOL", column]]

# Get gainers and losers
top_5_gainers = get_top(df, "%CHNG")
top_5_losers = get_bottom(df, "%CHNG")

print("Top 5 Gainers:\n", top_5_gainers)
print("\nTop 5 Losers:\n", top_5_losers)

# Plot gainers and losers
fig, ax = plt.subplots(1, 2, figsize=(14, 5))

sns.barplot(x="SYMBOL", y="%CHNG", data=top_5_gainers, ax=ax[0], palette="Greens_r")
ax[0].set_title("Top 5 Gainers")
ax[0].set_ylabel("% Change")
ax[0].set_xlabel("Stock Symbol")
ax[0].tick_params(axis='x', rotation=45)

sns.barplot(x="SYMBOL", y="%CHNG", data=top_5_losers, ax=ax[1], palette="Reds_r")
ax[1].set_title("Top 5 Losers")
ax[1].set_ylabel("% Change")
ax[1].set_xlabel("Stock Symbol")
ax[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()



top_5_in_last_30_days = get_top(df, "perChange30d")
print("\nTop 5 Stocks in Last 30 Days:\n", top_5_in_last_30_days)
print()

# Function to get stocks that are 30% below their 52-week high
def stocks_below_30_percent_high(df):
    if "LTP" in df.columns and "52W H" in df.columns:
        filtered_df = df[df["LTP"] <= 0.7 * df["52W H"]]
        return filtered_df[["SYMBOL", "LTP", "52W H"]]
    else:
        print("Error: 'LTP' or '52W H' column not found in DataFrame.")
        return pd.DataFrame()

# Function to get stocks that are 20% above their 52-week low
def stocks_above_20_percent_low(df):
    if "LTP" in df.columns and "52W L" in df.columns:
        filtered_df = df[df["LTP"] >= 1.2 * df["52W L"]]
        return filtered_df[["SYMBOL", "LTP", "52W L"]]
    else:
        print("Error: 'LTP' or '52W L' column not found in DataFrame.")
        return pd.DataFrame()

# Get filtered stocks
stocks_30_below_high = stocks_below_30_percent_high(df)
stocks_20_above_low = stocks_above_20_percent_low(df)

print("\nStocks 30% below 52W High:\n", stocks_30_below_high)
print("\nStocks 20% above 52W Low:\n", stocks_20_above_low)
