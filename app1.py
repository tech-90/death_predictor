import streamlit as st
import folium
from streamlit_folium import folium_static
import numpy as np
import pickle


from xgboost import XGBRegressor
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = XGBRegressor()
model.load_model(os.path.join(BASE_DIR, 'model.json'))




# Streamlit app
st.title("COVID-19 Predictions Based on Location")

# Create map
map = folium.Map(location=[20, 0], zoom_start=2)
coords = []

# Function to capture coordinates
def on_click(e):
    coords.append((e.latlng.lat, e.latlng.lng))
    st.session_state['coords'] = coords[-1]

map.add_child(folium.ClickForMarker(popup="Selected Location"))

# Display map
folium_static(map)

# Predict based on coordinates
if 'coords' in st.session_state:
    lat, lon = st.session_state['coords']
    st.write(f"### Selected Coordinates:")
    st.write(f"Latitude: {lat}, Longitude: {lon}")

    input_data = np.array([[lat, lon]])
    predicted_deaths = model1.predict(input_data)[0][0]
    predicted_cfr = model1.predict(input_data)[0][1]
    predicted_confirmed = model1.predict(input_data)[0][2]

    st.write("### Predictions:")
    st.write(f"- **Expected Deaths**: {predicted_deaths:.2f}")
    st.write(f"- **Case Fatality Rate (CFR)**: {predicted_cfr:.2f}%")
    st.write(f"- **Confirmed Cases**: {predicted_confirmed:.2f}")
