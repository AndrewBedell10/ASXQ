import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data['Avg_Price'] = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4.0
    return data['Avg_Price']

def calculate_cash_cover(start_date, end_date, starting_cash, quarterly_burn):
    starting_cash = float(starting_cash)
    quarterly_burn = float(quarterly_burn)

    daily_burn = quarterly_burn / 90.0

    date_range = pd.date_range(start=start_date, end=end_date)

    cash_values = []

    for date in date_range:
        if starting_cash > 0:
            cash_values.append(starting_cash)
            starting_cash -= daily_burn

    cash_cover_values = [cash / quarterly_burn for cash in cash_values]

    cash_cover_df = pd.DataFrame({
        'Date': date_range[:len(cash_cover_values)],
        'Cash Cover': cash_cover_values
    })

    # Filter date range to match stock data
    cash_cover_df = cash_cover_df[(cash_cover_df['Date'] >= start_date) & (cash_cover_df['Date'] <= end_date)]
    cash_cover_df.set_index('Date', inplace=True)

    return cash_cover_df

def plot_cash_cover_and_stock(ticker, start_date=None, end_date=None, q_release_date=None, placement_date=None, starting_cash=None, quarterly_burn=None):
    if start_date is None:
        start_date = '2023-09-30'
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    cash_cover_df = calculate_cash_cover(start_date, end_date, starting_cash, quarterly_burn)
    stock_data = fetch_stock_data(ticker, start_date, end_date)

    # Convert index to datetime for stock data
    stock_data.index = pd.to_datetime(stock_data.index)

    # Ensure both data frames have a consistent date index
    merged_df = pd.merge(stock_data, cash_cover_df, left_index=True, right_index=True, how='outer')

    # Filter merged data frame to include only weekdays with price data
    merged_df = merged_df[merged_df.index.isin(stock_data.index)]

    plt.figure(figsize=(12, 6))

    # Plot Stock Price
    ax1 = plt.subplot()
    ax1.plot(merged_df.index, merged_df['Avg_Price'], label=f"{ticker} Average Price", color='blue')
    ax1.set_xlabel("Date")
    ax1.set_ylabel(f"{ticker} Average Price", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create another y-axis for Cash Cover
    ax2 = ax1.twinx()
    ax2.plot(merged_df.index, merged_df['Cash Cover'], label="Cash Cover", color='green')
    ax2.set_ylabel("Cash Cover", color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Draw vertical line at the date when Cash Cover equals 1 (red)
    cash_cover_1_date = merged_df[merged_df['Cash Cover'] < 1].index[0]
    ax2.axvline(x=cash_cover_1_date, color='red', linestyle='--', linewidth=2)

    # Draw vertical line at the Q Release Date (orange)
    if q_release_date:
        ax2.axvline(x=pd.to_datetime(q_release_date), color='orange', linestyle='--', linewidth=2)

    # Draw vertical line at the Placement Date (grey)
    if placement_date:
        ax2.axvline(x=pd.to_datetime(placement_date), color='grey', linestyle='--', linewidth=2)

    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc=0)

    plt.title(f"Cash Cover and {ticker} Average Price Over Time")
    plt.grid(True)
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

# Input parameters
ticker = input("Enter Stock Ticker (e.g., AAPL for Apple): ")
start_date = input("Enter Start Date (YYYY-MM-DD) (Optional, press Enter to skip): ") or None
end_date = input("Enter End Date (YYYY-MM-DD) (Optional, press Enter to skip): ") or None
q_release_date = input("Enter Q Release Date (YYYY-MM-DD) (Optional, press Enter to skip): ") or None
placement_date = input("Enter Placement Date (YYYY-MM-DD) (Optional, press Enter to skip): ") or None
starting_cash = input("Enter Starting Cash (Optional, press Enter to skip): ") or None
quarterly_burn = input("Enter Quarterly Burn (Optional, press Enter to skip): ") or None

# Check if Ticker is provided
if ticker:
    plot_cash_cover_and_stock(ticker, start_date, end_date, q_release_date, placement_date, starting_cash, quarterly_burn)
else:
    # Display charts for ARR.AX, GLN.AX, and HAS.AX based on the provided table
    tickers_data = {
        'ARR.AX': {'q_release_date': '1/29/24', 'placement_date': '2/23/24', 'starting_cash': '6.3', 'quarterly_burn': '3'},
        'GLN.AX': {'q_release_date': '1/31/24', 'placement_date': '1/31/2024', 'starting_cash': '30', 'quarterly_burn': '15'},
        'HAS.AX': {'q_release_date': '1/30/24', 'placement_date': '3/27/2024', 'starting_cash': '42', 'quarterly_burn': '24'}
    }

    for ticker, data in tickers_data.items():
        plot_cash_cover_and_stock(ticker, start_date, end_date, data['q_release_date'], data['placement_date'], data['starting_cash'], data['quarterly_burn'])

