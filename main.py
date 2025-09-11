import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Set layout to wide
st.set_page_config(layout="wide")

excel_file = "records.xlsx"

required_columns = [
    "Type", "Date", "Year", "Month", "Day Number", "Day Name",
    "Subtype", "Goal", "Simple Unit",
    "Description", "Composite Unit", "Completed",
    "Entry Timestamp"
]

# Create or load Excel
if os.path.exists(excel_file):
    try:
        df = pd.read_excel(excel_file, engine="openpyxl")
    except Exception:
        df = pd.DataFrame(columns=required_columns)
        df.to_excel(excel_file, index=False, engine="openpyxl")
else:
    df = pd.DataFrame(columns=required_columns)
    df.to_excel(excel_file, index=False, engine="openpyxl")
    st.warning("⚠️ Excel file not found. A new one has been created.")

st.title("🌿 Nutrition & Activity Tracker 🏃🥗")

# <-- Type OUTSIDE the form so that changing it updates UI immediately -->
record_type = st.selectbox("Type", ["Meal", "Stretch"])

with st.form("entry_form"):
    date = st.date_input("Date")
    year = date.year
    month = date.strftime("%B")
    day_number = date.day
    day_name = date.strftime("%A")

    if record_type == "Meal":
        subtype = st.selectbox("Subtype", ["Breakfast", "Lunch", "Snack", "Dinner"])
        goal = st.text_input("Ingredient")
        simple_unit = st.text_input("Simple Unit (e.g. 150 g)")
        description = st.text_input("Description")
        composite_unit = st.text_input("Composite Unit (e.g. 1 portion)")
    else:  # Stretch
        subtype = st.selectbox("Subtype", ["Foam Roller", "Band", "Standard", "Yoga"])
        goal = st.text_input("Stretch Type")
        simple_unit = st.text_input("Duration (e.g. 10 min)")
        description = st.text_input("Target Body Part")
        composite_unit = st.text_input("Intensity (Low/Medium/High)")

    submit = st.form_submit_button("Save")

# Action after form submission
if submit:
    new_entry = {
        "Type": record_type,
        "Date": date.strftime("%d/%m/%Y"),
        "Year": year,
        "Month": month,
        "Day Number": day_number,
        "Day Name": day_name,
        "Subtype": subtype,
        "Goal": goal,
        "Simple Unit": simple_unit,
        "Description": description,
        "Composite Unit": composite_unit,
        "Completed": "No",  # normal form entry = not auto completed
        "Entry Timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_excel(excel_file, index=False, engine="openpyxl")
    st.success("✅ Record saved successfully")
    df = pd.read_excel(excel_file, engine="openpyxl")

# ---- Global Completed Option ----
st.subheader("✅ Mark All as Completed")
completed_choice = st.radio("Do you want to auto-complete all subtypes?", ["No", "Yes"])

if completed_choice == "Yes":
    now = datetime.now()
    if record_type == "Meal":
        subtypes = ["Breakfast", "Lunch", "Snack", "Dinner"]
    else:  # Stretch
        subtypes = ["Foam Roller", "Band", "Standard", "Yoga"]

    auto_entries = []
    for stype in subtypes:
        auto_entries.append({
            "Type": record_type,
            "Date": now.strftime("%d/%m/%Y"),
            "Year": now.year,
            "Month": now.strftime("%B"),
            "Day Number": now.day,
            "Day Name": now.strftime("%A"),
            "Subtype": stype,
            "Goal": "",
            "Simple Unit": "",
            "Description": "",
            "Composite Unit": "",
            "Completed": "Yes",
            "Entry Timestamp": now.strftime("%d/%m/%Y %H:%M:%S")
        })

    df = pd.concat([df, pd.DataFrame(auto_entries)], ignore_index=True)
    df.to_excel(excel_file, index=False, engine="openpyxl")
    st.success(f"✅ {len(subtypes)} records added automatically as completed")
    df = pd.read_excel(excel_file, engine="openpyxl")

# Show records
st.subheader("📄 Current Records")
st.dataframe(df)

# Delete functionality
st.subheader("🗑️ Delete a Record")
if len(df) > 0:
    index_to_delete = int(st.number_input(
        "Enter the row index to delete",
        min_value=0, max_value=len(df)-1, value=0, step=1
    ))
    if st.button("Delete"):
        df = df.drop(index_to_delete).reset_index(drop=True)
        df.to_excel(excel_file, index=False, engine="openpyxl")
        st.success(f"✅ Record at index {index_to_delete} deleted.")
        df = pd.read_excel(excel_file, engine="openpyxl")
else:
    st.info("No records available to delete.")
