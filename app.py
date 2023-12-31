import os
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re

# Set Streamlit page configuration
st.set_page_config(page_title="Answer Socrates Helper", page_icon="🔍", layout="wide")

# Fetch API key and CSE ID from environment variables or hardcoded values
api_key = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")
cse_id = os.environ.get("CUSTOM_SEARCH_ENGINE_ID", "YOUR_CSE_ID_HERE")

def google_search(query, api_key, cse_id, num=3):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {'q': query, 'key': api_key, 'cx': cse_id, 'num': num}
    response = requests.get(url, params=params)
    return json.loads(response.text)

def extract_bold_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    bold_texts = soup.find_all(['strong', 'b'])
    return [text.get_text().strip() for text in bold_texts]

@st.cache(allow_output_mutation=True)
def process_queries(uploaded_file, api_key, cse_id):
    df = pd.read_csv(uploaded_file)  # Assuming CSV, modify for Excel if needed
    queries = df['Query']  # Replace 'Query' with the actual column name in your CSV

    results = []
    for query in queries:
        search_results = google_search(query, api_key, cse_id)
        top_3_links = [item['link'] for item in search_results.get('items', [])[:3]]
        bold_text = []
        for link in top_3_links:
            try:
                page_content = requests.get(link).text
                bold_text += extract_bold_text(page_content)
            except Exception as e:
                print(f"Error fetching bold text from {link}: {e}")
        # Guess content type here, currently placeholder
        content_type_guess = "Article"  # Placeholder, implement actual guessing logic
        results.append([query] + bold_text + top_3_links + [content_type_guess])

    columns = ['Query', 'Bold Text 1', 'Bold Text 2', 'Bold Text 3', 'Link 1', 'Link 2', 'Link 3', 'Content Type Guess']
    return pd.DataFrame(results, columns=columns)

st.title("Answer Socrates Helper")

uploaded_file = st.file_uploader("Upload the Answer Socrates Sheet", type=['csv'])

if uploaded_file is not None:
    result_df = process_queries(uploaded_file, api_key, cse_id)
    st.dataframe(result_df)

    csv_result = result_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Results", data=csv_result, file_name="socrates_results.csv", mime="text/csv")
