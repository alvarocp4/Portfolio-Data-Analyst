import streamlit as st
import pandas as pd
import os

# Excel file name
excel_file = "records.xlsx"

# Create the file if it doesn't exist
if not os.path.exists(excel_file):
    initial_df = pd.DataFrame(columns=["Name", "Age", "Email"])
    initial_df.to_excel(excel_file, index=False)

# App title
st.title("📋 Data Entry to Excel")

# Input form
with st.form("data_entry_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    email = st.text_input("Email")
    submit = st.form_submit_button("Save")

    if submit:
        # Load existing data
        df = pd.read_excel(excel_file)
        # Add new record
        new_record = pd.DataFrame([[name, age, email]], columns=df.columns)
        df = pd.concat([df, new_record], ignore_index=True)
        # Save to Excel
        df.to_excel(excel_file, index=False)
        st.success("✅ Record saved successfully!")

# Display saved records
if st.checkbox("Show saved records"):
    df = pd.read_excel(excel_file)
    st.dataframe(df)
