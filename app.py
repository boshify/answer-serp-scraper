import streamlit as st
import pandas as pd
import requests
import json

# Function to perform a search using the Google Custom Search API
def search(query, api_key, cse_id, **kwargs):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
    }
    params.update(kwargs)
    response = requests.get(url, params=params)
    return json.loads(response.text)

# Function to process the file and add new columns with search result titles
def process_file(file, api_key, cse_id):
    df = pd.read_csv(file)

    # Add new columns for search result titles
    df['SERP Title 1'] = ''
    df['SERP Title 2'] = ''
    df['SERP Title 3'] = ''

    # Iterate over each row and perform search
    for index, row in df.iterrows():
        query = row['C']  # Using the search queries from column C
        results = search(query, api_key, cse_id)

        # Extract and assign the titles of the top 3 search results
        for i in range(3):
            if results.get('items') and len(results['items']) > i:
                df.at[index, f'SERP Title {i+1}'] = results['items'][i].get('title', '')

    return df

# Streamlit app layout
def main():
    st.title("Spreadsheet Processor")
    api_key = st.text_input("Enter your Google API Key")
    cse_id = st.text_input("Enter your Custom Search Engine ID")

    uploaded_file = st.file_uploader("Upload your file", type=["csv"])

    if uploaded_file is not None and api_key and cse_id:
        processed_data = process_file(uploaded_file, api_key, cse_id)

        st.write("Processed Data:")
        st.write(processed_data)

        # Download button
        st.download_button(
            label="Download processed data",
            data=processed_data.to_csv(index=False),
            file_name="processed_data.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
