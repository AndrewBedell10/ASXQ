import streamlit as st
import pandas as pd
import requests
import io

# Function to fetch data from GitHub CSV file
def load_data_from_github(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        content = response.content.decode('utf-8')
        
        # Try reading the CSV with various parameters to handle potential issues
        try:
            df = pd.read_csv(io.StringIO(content))
        except pd.errors.ParserError:
            try:
                df = pd.read_csv(io.StringIO(content), delimiter=';')  # Try semicolon delimiter
            except pd.errors.ParserError:
                df = pd.read_csv(io.StringIO(content), engine='c', error_bad_lines=False)  # Skip bad lines
        
        return df
    except Exception as e:
        st.error(f"Error loading data from {url}: {e}")
        return None

# GitHub CSV URL
github_csv_url = 'https://github.com/AndrewBedell10/ASXQ/blob/main/Quarterly%204Q2023%20Example.csv'  # Replace with your GitHub CSV URL

# Streamlit app
def main():
    st.title('CSV File Viewer')
    
    # Load data from GitHub
    df = load_data_from_github(github_csv_url)
    
    if df is not None:
        # Display DataFrame as table
        st.write("### Table from CSV File")
        st.write(df)

if __name__ == '__main__':
    main()
