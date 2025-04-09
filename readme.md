# 📊 NSE Stock Market Analysis Tool

This Python script fetches real-time stock data for the **NIFTY 50 Index** from the **NSE India API**, analyzes it, and visualizes:

- Top 5 gainers & losers by % change  
- Top 5 stocks by 30-day performance  
- Stocks trading **30% below 52-week high**  
- Stocks trading **20% above 52-week low**

The tool logs all steps and outputs a comparative chart of gainers and losers.

---

## ⚙️ Features

- 🔁 **Live Data**: Fetched using the official [NSE India API](https://www.nseindia.com)
- 🧼 **Cleaned and Structured Data**: Prepares a usable pandas DataFrame
- 📈 **Analytics**:
  - Top 5 gainers/losers by % daily change
  - Top 5 gainers over the last 30 days
  - Stocks trading 30% below their 52-week highs
  - Stocks trading 20% above their 52-week lows
- 📊 **Visualization**:
  - Generates bar charts for top gainers and losers
- 📜 **Logging**:
  - Every important step is logged in `stock_analysis.log`

---

## 🐍 Requirements

Install dependencies using pip:

```bash
pip install requests pandas matplotlib seaborn
```

---

## 🚀 How It Works

### 1. **Fetch Data**
- Sends a request to NSE API with browser-like headers.
- Retrieves the **NIFTY 50** stock data.

### 2. **Data Cleaning**
- Renames and filters key columns:
  - `SYMBOL`, `LTP`, `%CHNG`, `52W H`, `52W L`, `30 D %CHNG`
- Converts all numeric fields safely.

### 3. **Analysis**
- Identifies:
  - Top 5 daily gainers & losers
  - Best 30-day performers
  - Undervalued (30% below 52W high)
  - Recovered (20% above 52W low)

### 4. **Plotting**
- Saves a dual bar chart in `gainers_losers_chart.png`.

---

## 📂 Output

- `stock_analysis.log`: Logs of the complete analysis
- `gainers_losers_chart.png`: Bar plot comparing gainers and losers

---

## 📌 Note

- NSE blocks automated bots aggressively. The script makes an initial session call to fetch cookies before accessing API data.
- Use responsibly and avoid excessive calls.

---

## 🧠 Sample Use Cases

- Building a stock alert system
- Filtering value stocks based on technical indicators
- Visualizing short-term vs long-term gainers

---

## 📬 Suggestions / Improvements?

The script is modular. You can easily add:
- Moving averages or RSI
- Sector-based filtering
- Export to Excel or Database

Feel free to fork and customize!
