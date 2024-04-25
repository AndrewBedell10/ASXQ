import streamlit as st
import pandas as pd
import os

# Get the current working directory
cwd = os.getcwd()

pd.options.display.float_format = '{:.2f}'.format

st.set_page_config(
    page_title='📊 ASX',
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)

st.title("📊 ASX")

# Load the Excel file into a DataFrame
file_path = os.path.join(cwd, "data.xlsx") 
df = pd.read_excel(file_path)


st.subheader("Browse all")
# Display the DataFrame
st.data_editor(df)

st.subheader("Select one")
col1, col2 = st.columns(2)
with col1:
    st.write("Company Name")
    company_name = st.selectbox(
        'Choose a Company',
        df['Company Name'].sort_values().unique().tolist(),
        index=None,
        placeholder='start typing...'
    )


if company_name != None:

    st.data_editor(df[df['Company Name'] == company_name].transpose())

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Company Market Cap (AUD)", value = '{:,.1f}'.format(df[df['Company Name'] == company_name][df.columns[2]].values[0]))

    with col2:
        st.metric(label="Average Daily Value Traded - 52 Weeks (AUD)", value = '{:,.1f}'.format(df[df['Company Name'] == company_name][df.columns[3]].values[0]))

    with col3:
        st.metric(label="""Cash from Investing Activities, Cumulative
    (0FQ, FY0, AUD)""",
                  value='{:,.1f}'.format(df[df['Company Name'] == company_name][df.columns[15]].values[0]))


    st.write(f'Info: {df[df['Company Name'] == company_name]["Business Description"].values[0]}')
