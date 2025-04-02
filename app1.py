import streamlit as st
import folium
from streamlit_folium import folium_static, st_folium
import numpy as np
import os
from joblib import load
from sklearn.neighbors import KNeighborsRegressor  # Ensure KNN is used

# Load the KNN model
BASE_DIR = os.getcwd()
model_path = os.path.join(BASE_DIR, 'KNN_model.joblib')

try:
    model = load(model_path)
except Exception as e:
    st.error(f"Error loading model: {e}")
    model = None

# Streamlit app
st.title("Virus Spread Predictions Based on Location")

# Create and display map
map = folium.Map(location=[20, 0], zoom_start=2)
map.add_child(folium.LatLngPopup())
clicked_point = st_folium(map, width=700, height=450)

if clicked_point and clicked_point.get("last_clicked"):
    lat = clicked_point["last_clicked"]["lat"]
    lon = clicked_point["last_clicked"]["lng"]

    st.write(f"### Selected Coordinates:")
    st.write(f"Latitude: {lat}, Longitude: {lon}")

    if model:
        # Prepare input and make prediction
        input_data = np.array([[lat, lon]])
        predicted = model.predict(input_data)

        st.write(f"- **Expected Deaths**: {predicted[0]}")
    else:
        st.warning("Model is not loaded. Please check the file path.")

