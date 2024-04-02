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
        
        # Read CSV content into a DataFrame
        df = pd.read_csv(io.StringIO(content))
        
        return df
    except Exception as e:
        st.error(f"Error loading data from {url}: {e}")
        return None

# GitHub CSV URL
github_csv_url = 'https://raw.githubusercontent.com/AndrewBedell10/ASXQ/main/Quarterly%204Q2023%20Example.csv'  # Replace with your GitHub CSV URL

# Streamlit app
def main():
    st.title('Company Data Viewer')
    
    # Load data from GitHub
    df = load_data_from_github(github_csv_url)
    
    if df is not None:
        # Display Main Table
        st.write("### Main Table")
        st.write(df)
        
        # Create Company Profile pages
        if 'Company Name' in df.columns:  # Check if the correct column name exists
            unique_companies = df['Company Name'].unique()
            selected_company = st.selectbox('Select Company:', unique_companies)
            
            if selected_company:
                st.write(f"### Company Profile: {selected_company}")
                
                # Create Company Table
                company_data = df[df['Company Name'] == selected_company].squeeze().drop('Company Name')
                company_df = pd.DataFrame({'Attribute': company_data.index, 'Value': company_data.values})
                
                st.write(company_df)
        else:
            st.error("Column 'Company Name' not found in the DataFrame.")

if __name__ == '__main__':
    main()
