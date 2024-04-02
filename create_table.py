import streamlit as st
import pandas as pd
import requests
import io

# Function to fetch data from GitHub CSV file
def load_data_from_github(url):
    response = requests.get(url)
    content = response.content.decode('utf-8')
    df = pd.read_csv(io.StringIO(content))
    return df

# GitHub CSV URL
github_csv_url = 'https://raw.githubusercontent.com/your-username/your-repo/main/Quarterly_4Q2023_Example.csv'  # Replace with your GitHub CSV URL

# Load data
try:
    df = load_data_from_github(github_csv_url)
    st.write("### Company Data Table")
    st.write(df)
except Exception as e:
    st.write(f"Error loading data: {e}")

