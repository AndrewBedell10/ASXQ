import streamlit as st
import pandas as pd
import requests
import io

# Function to fetch data from GitHub CSV file with custom column names
def load_data_from_github(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        content = response.content.decode('utf-8')
        
        # Define custom column names
        custom_column_names = {
            'Net Cash from / (used in) Operating Activities': 'CFO',
            'Cash Flows from Operating Activities, Financing Activities, and Investing Activities': 'CFI',
            'Net Increase / (Decrease) in Cash and Cash Equivalents': 'CFF',
            'Cash and Cash Equivalents at Beginning of Period': 'Cash Balance',
            'Cash and Cash Equivalents at End of Period': 'Cash Balance'
        }
        
        # Read CSV content into a DataFrame with custom column names
        df = pd.read_csv(io.StringIO(content), names=custom_column_names.values(), header=0)
        
        # Rename the columns to the desired custom names
        df.rename(columns=custom_column_names, inplace=True)
        
        return df
    except Exception as e:
        st.error(f"Error loading data from {url}: {e}")
        return None

# GitHub CSV URL
github_csv_url = 'https://raw.githubusercontent.com/AndrewBedell10/ASXQ/main/Quarterly%204Q2023%20Example.csv'  # Replace with your GitHub CSV URL

# Streamlit app
def main():
    st.title('Company Data Viewer')
    
    # Load data from GitHub with custom column names
    df = load_data_from_github(github_csv_url)
    
    if df is not None:
        # Display Main Table
        st.write("### Main Table")
        st.write(df)
        
        # Print list of column names
        st.write("### Actual Column Names")
        st.write(df.columns.tolist())
        
        # Create Company Profile pages
        if 'Company Name' in df.columns:  # Check if the correct column name exists
            unique_companies = df['Company Name'].unique()
            selected_company = st.selectbox('Select Company:', unique_companies)
            
            if selected_company:
                # Identify correct column name for ticker symbol
                ticker_column = [col for col in df.columns if 'Ticker' in col]
                if ticker_column:
                    ticker = df[df['Company Name'] == selected_company][ticker_column[0]].iloc[0]
                    profile_title = f"### Company Profile: {selected_company} | {ticker}"
                    st.write(profile_title)
                    
                    # Create Company Table
                    company_data = df[df['Company Name'] == selected_company].squeeze().drop(['Company Name', ticker_column[0]])
                    company_df = pd.DataFrame({'Attribute': company_data.index, 'Value': company_data.values})
                    
                    st.write(company_df)
                else:
                    st.error("Column for ticker symbol not found in the DataFrame.")
        else:
            st.error("Column 'Company Name' not found in the DataFrame.")

if __name__ == '__main__':
    main()
