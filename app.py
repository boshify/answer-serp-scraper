import streamlit as st
import pandas as pd

# Function to add new columns with placeholder text
def process_file(file):
    df = pd.read_csv(file)
    df['Content Type'] = 'banana'  # Adding 'Content Type' column
    df['SERP Title 1'] = 'banana'  # Adding 'SERP Title 1' column
    df['SERP Title 2'] = 'banana'  # Adding 'SERP Title 2' column
    df['SERP Title 3'] = 'banana'  # Adding 'SERP Title 3' column
    df['Bold Text'] = 'banana'     # Adding 'Bold Text' column
    return df

# Streamlit app layout
def main():
    st.title("Spreadsheet Processor")

    uploaded_file = st.file_uploader("Upload your file", type=["csv"])

    if uploaded_file is not None:
        processed_data = process_file(uploaded_file)

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
