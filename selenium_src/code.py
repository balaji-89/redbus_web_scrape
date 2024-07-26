import streamlit as st
import pandas as pd
import mysql.connector
from sql_src.code import fetch_data


def app():
    """
    Description: Loads the home page of our streamlit application
    """
    st.title("Bus Information")
    df = fetch_data()
    st.sidebar.header("Filters")
    route = st.sidebar.selectbox("Select Route", ["All"] + df['route'].unique().tolist())
    bus_type = st.sidebar.selectbox("Select Bus Type", ["All"] + df['bus_type'].unique().tolist())

    min_price, max_price = int(df['price'].min()), int(df['price'].max())
    price_range = st.sidebar.slider("Select Price Range", min_price, max_price, (min_price, max_price))

    min_rating, max_rating = float(df['rating'].min()), float(df['rating'].max())
    star_rating = st.sidebar.slider("Select Star Rating", min_rating, max_rating, (min_rating, max_rating))

    availability = st.sidebar.selectbox("Select Availability", ["All", "Available", "Not Available"])

    if route != "All":
        df = df[df['route'] == route]
    if bus_type != "All":
        df = df[df['bus_type'] == bus_type]
    df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]
    df = df[(df['rating'] >= star_rating[0]) & (df['rating'] <= star_rating[1])]
    if availability == "Available":
        df = df[df['available_seats'] > 0]
    elif availability == "Not Available":   
        df = df[df['available_seats'] == 0]

    st.write(f"Displaying {len(df)} results")
    st.dataframe(df[['bus_name', 'route', 'bus_type', 'duration', 'departure_time', 'reaching_time', 'price', 'available_seats', 'rating']], 
                 width=2500)

if __name__ == "__main__":
    app()
