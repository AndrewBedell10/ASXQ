import requests
from bs4 import BeautifulSoup
import pandas as pd

# pip install requests beautifulsoup4 pandas


# Base URL for the pages


base_url = "https://www.weblink.com.au/news/news.asp"
params = {
    "mode": "Ann",
    "page_size": 150,
    "cat": "",
    "search_by1": "code",
    "SearchString1": "",
    "onlySensitive": "on",
    "dateEQ": "",
    "id": "andrew.bedell10",
    "pw": "ASX-Q2024",
}
# Function to extract table data from a page
def extract_table_data(soup):
    table_data = []
    table = soup.find('table', {'class': 'contentarea'})  # Adjust class name as needed

    if table:
        rows = table.find_all('tr')

        # Extract header row if it exists
        headers = [header.get_text(strip=True) for header in rows[0].find_all('th')]

        # Append the header row if it exists
        if headers:
            table_data.append(headers)
            data_rows = rows[1:]
        else:
            data_rows = rows

        # Extract data rows
        for row in data_rows:
            columns = row.find_all('td')
            columns = [col.get_text(strip=True) for col in columns]
            if columns:
                table_data.append(columns)

    return table_data

# Initialize a list to store all the table data
all_table_data = []
headers = None
max_columns = 0

# Loop through the first 15 pages (adjust the range as needed)
for page_num in range(15):
    params["pager"] = page_num * 150
    response = requests.get(base_url, params=params)
    print(f"Page {page_num + 1} extracted.")

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        page_data = extract_table_data(soup)

        if page_data:
            if headers is None:
                headers = page_data[0]
                max_columns = len(headers)
            initial_len = len(all_table_data)
            for row in page_data[1:]:
                # Update max_columns to the maximum length of rows encountered
                max_columns = max(max_columns, len(row))
                all_table_data.append(row)

            # Check if new rows with non-empty "Symbol" were added
            if all(len(row) <= headers.index('Symbol') or not row[headers.index('Symbol')].strip() for row in
                   page_data[1:]):
                print(
                    f"No new records with non-empty 'Symbol' added on page {page_num + 1}. Stopping further requests.")
                break
    else:
        print(f"Failed to retrieve page {page_num + 1}. Status code: {response.status_code}")

# Pad rows with fewer columns than max_columns with empty strings
for i in range(len(all_table_data)):
    if len(all_table_data[i]) < max_columns:
        all_table_data[i].extend([''] * (max_columns - len(all_table_data[i])))

# Update headers to match max_columns if necessary
if len(headers) < max_columns:
    headers.extend([''] * (max_columns - len(headers)))

# Convert the combined data into a pandas DataFrame
if all_table_data:
    df = pd.DataFrame(all_table_data, columns=headers)

    # Display the DataFrame
    df = df[df['Symbol'].str.strip() != '']

    # Drop the first 'Headline', 'Pages', and 'Info' columns
    df = df.drop(['Info', 'Headline', 'Pages'], axis=1)

    # Rename the remaining 'Headline' and 'Pages' columns
    df.columns = df.columns[:-2].tolist() + ['Headline', 'Pages']
    df = df.loc[:, df.columns.str.strip() != '']

    # Find symbols with "Trading Halt" in the "Headline"
    trading_halt_symbols = df[df['Headline'].str.contains('Trading Halt', case=False, na=False)]['Symbol'].unique()

    # Filter DataFrame to keep all rows for these symbols
    df = df[df['Symbol'].isin(trading_halt_symbols)]

    # Save the updated DataFrame to a new Excel file
    output_file = 'placements.xlsx'
    df.to_excel(output_file, index=False)
    unique_symbols = df['Symbol'].nunique()
    print(f"Unique number of symbols: {unique_symbols}")

else:
    print("No data extracted.")
