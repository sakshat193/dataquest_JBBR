import streamlit as st
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

# Load the pre-saved components from the same directory as the app
base_path="Notebooks/Predictions_Training/Models/"

with open(os.path.join(base_path, "scaler.pkl"), "rb") as f:
    scaler = pickle.load(f)

with open(os.path.join(base_path, "best_rfc_model.pkl"), "rb") as f:
    best_rfc = pickle.load(f)

# Function to encode alert levels
def encode_alert(alert):
    alert_mapping = {
        "No alert": 0,
        "green": 1,
        "yellow": 2,
        "orange": 3,
        "red": 4
    }
    return alert_mapping.get(alert, 0)

# Function to predict using the model
def predict(inputs):
    # Standardize the inputs
    inputs_scaled = scaler.transform([inputs])
    
    # Make prediction
    prediction = best_rfc.predict(inputs_scaled)
    return prediction[0]

# Streamlit page layout
st.title("Earthquake Significance Prediction")

# User input: form for magnitude, mmi, cdi, alert, latitude, and longitude
magnitude = st.slider("Magnitude", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
mmi = st.slider("MMI", min_value=1, max_value=10, value=6, step=1)  # MMI starts from 1
cdi = st.slider("CDI", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
alert_options = ['No alert', 'Green', 'Yellow', 'Orange', 'Red']
alert = st.selectbox("Select Alert Level", alert_options)
latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=0.0)
longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=0.0)

# When the user clicks on 'Predict'
if st.button("Predict"):
    # Encode alert
    encoded_alert = encode_alert(alert)
    
    # Prepare input data
    input_data = [magnitude, mmi, cdi, encoded_alert, latitude, longitude]
    
    # Make prediction
    result = predict(input_data)
    st.write(f"The predicted significance is: {result:.2f}")
