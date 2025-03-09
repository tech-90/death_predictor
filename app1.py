import streamlit as st
import folium
from streamlit_folium import folium_static
import numpy as np
import pickle
from streamlit_folium import st_folium


from xgboost import XGBRegressor
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = XGBRegressor()
model.load_model(os.path.join(BASE_DIR, 'model.json'))




# Streamlit app
st.title("COVID-19 Predictions Based on Location")

# Create map
map = folium.Map(location=[20, 0], zoom_start=2)

# Add click marker to the map
map.add_child(folium.LatLngPopup())

# Display map and capture click
clicked_point = st_folium(map, width=700, height=450)

if clicked_point and clicked_point.get("last_clicked"):
    lat = clicked_point["last_clicked"]["lat"]
    lon = clicked_point["last_clicked"]["lng"]

    st.write(f"### Selected Coordinates:")
    st.write(f"Latitude: {lat}, Longitude: {lon}")

    # Predict based on clicked coordinates
    input_data = np.array([[lat, lon]])
    predicted = model.predict(input_data)[0]
    
    predicted_deaths = predicted[0]
    predicted_cfr = predicted[1]
    predicted_confirmed = predicted[2]

    st.write("### Predictions:")
    st.write(f"- **Expected Deaths**: {predicted_deaths:.2f}")
    st.write(f"- **Case Fatality Rate (CFR)**: {predicted_cfr:.2f}%")
    st.write(f"- **Confirmed Cases**: {predicted_confirmed:.2f}")