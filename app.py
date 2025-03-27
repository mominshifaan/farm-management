import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Initialize database
def init_db():
    conn = sqlite3.connect('farm_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS crops
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                crop_name TEXT NOT NULL,
                planting_date DATE NOT NULL,
                harvest_date DATE,
                cost REAL DEFAULT 0,
                revenue REAL DEFAULT 0)''')
    conn.commit()

def main():
    init_db()
    st.set_page_config(page_title="Farm Manager", layout="wide")
    st.title("🌱 My Farm Management System")
    
    # Input form
    with st.form("crop_form"):
        st.write("**Add New Crop**")
        crop = st.text_input("Crop Name*")
        planted = st.date_input("Planting Date*", datetime.today())
        harvested = st.date_input("Harvest Date")
        cost = st.number_input("Cost ($)", min_value=0.0, value=0.0)
        revenue = st.number_input("Revenue ($)", min_value=0.0, value=0.0)
        
        if st.form_submit_button("Save"):
            if crop:
                conn = sqlite3.connect('farm_data.db')
                conn.execute("""INSERT INTO crops 
                              (crop_name, planting_date, harvest_date, cost, revenue)
                              VALUES (?,?,?,?,?)""",
                           (crop, planted, harvested, cost, revenue))
                conn.commit()
                st.success("Saved!")
            else:
                st.error("Please enter crop name")
    
    # Display data
    st.header("Your Records")
    df = pd.read_sql("SELECT * FROM crops", sqlite3.connect('farm_data.db'))
    if not df.empty:
        df['profit'] = df['revenue'] - df['cost']
        st.dataframe(df)
        st.metric("Total Profit", f"${df['profit'].sum():,.2f}")

if __name__ == "__main__":
    main()
  
