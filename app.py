import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Flight Data Analytics", layout="wide")

st.title("✈️ Flight Pricing Data Analytics")
st.markdown("This dashboard connects to a FastAPI backend that queries a SQLite database and runs ML models.")

API_URL = "http://localhost:8000"

st.header("1. Historical Pricing by Airline")
if st.button("Fetch Airline Averages"):
    try:
        response = requests.get(f"{API_URL}/api/analytics/airlines")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(df)
            
            with col2:
                st.bar_chart(df, x="airline", y="avg_price")
        else:
            st.error("Failed to fetch data from API")
    except requests.exceptions.ConnectionError:
        st.error("API is not running. Please start the FastAPI server first.")

st.divider()

st.header("2. AI Price Trend Analysis (Linear Regression)")
st.markdown("Uses Machine Learning to calculate how much prices jump as the departure date approaches.")

# Let user select an airline to analyze, or leave blank for all
airline_input = st.selectbox("Select Airline to Analyze (or all)", 
                             ["All", "Vistara", "Air India", "Indigo", "SpiceJet", "GoFirst", "AirAsia"])

if st.button("Calculate Trend"):
    try:
        params = {}
        if airline_input != "All":
            params["airline"] = airline_input
            
        response = requests.get(f"{API_URL}/api/analytics/trend", params=params)
        
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                st.warning(data["error"])
            else:
                st.success(f"Successfully analyzed {data['data_points']} flights.")
                st.metric(
                    label=f"Daily Price Increase ({data['airline_analyzed']})", 
                    value=f"₹ {data['price_increase_per_day_closer']} / day",
                    delta="Cost goes up as you wait!"
                )
        else:
            st.error("Failed to fetch data from API")
    except requests.exceptions.ConnectionError:
        st.error("API is not running. Please start the FastAPI server first.")
