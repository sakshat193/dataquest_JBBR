import streamlit as st
import pickle
import pandas as pd
from geopy.geocoders import Nominatim
import time

def significance():
    st.title("Earthquake Event Significance Predictor")
    st.write("This page predicts the significance of earthquake events based on input features.")
   

# Load pre-trained significance prediction model and transformers
def load_pickle(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

# Convert latitude and longitude to a location
def get_location(lat, lon):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        coords = f"{lat}, {lon}"
        location = geolocator.reverse(coords, language='en')
        if location and location.raw.get('address'):
            address = location.raw['address']
            state = (
                address.get('state_en') or 
                address.get('state') or 
                address.get('province_en') or 
                address.get('province') or 
                ''
            )
            country = address.get('country_en') or address.get('country', '')
            return f"{state}, {country}".strip(', ')
        return "Unknown Location"
    except Exception as e:
        print(f"Error getting location for coordinates {lat}, {lon}: {e}")
        return "Error retrieving location"

# Streamlit App
def main():
    st.title("Earthquake Event Significance Predictor")

    st.markdown("""
    This tool takes input features like `alert`, `magnitude`, `longitude`, `latitude`, and `cdi`, 
    determines the location based on the coordinates, and predicts the significance of the event.
    """)

    # Alert slider with labels
    alert_labels = {0: "No Alert", 1: "Green", 2: "Yellow", 3: "Orange", 4: "Red"}
    alert_value = st.slider("Alert Level", min_value=0, max_value=4, step=1, value=0, format="%d")
    alert = alert_value  # Alert value is numeric for the model, but we display the label
    st.write(f"Selected Alert Level: **{alert_labels[alert_value]}**")

    # Input fields for other features
    magnitude = st.number_input("Magnitude of Earthquake", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
    longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=0.0, step=0.1)
    latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=0.0, step=0.1)
    cdi = st.number_input("CDI (Community Determined Intensity)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

    # Convert longitude and latitude to location
    location = get_location(latitude, longitude)
    st.write(f"**Location:** {location}")

    # Button to predict the significance
    if st.button("Predict Significance"):
        try:
            # Load the model and transformers
            model_path = "Predictions_Training/Models/sig_model.pkl"
            transformers_path = "Predictions_Training/Models/sig_transformers.pkl"
            selected_features_path = "Predictions_Training/Models/sig_selected_features.pkl"

            model = load_pickle(model_path)
            transformers = load_pickle(transformers_path)
            selected_features = load_pickle(selected_features_path)

            # Create a DataFrame with user input
            input_data = pd.DataFrame({
                "alert": [alert],
                "magnitude": [magnitude],
                "longitude": [longitude],
                "latitude": [latitude],
                "cdi": [cdi]
            })

            # Transform data if transformers exist
            for transformer in transformers:
                input_data = transformer.transform(input_data)

            # Select only the required features
            input_data = input_data[selected_features]

            # Predict significance
            significance = model.predict(input_data)[0]

            st.success(f"Predicted Significance: {significance}")

        except FileNotFoundError:
            st.error("Model or transformers not found. Please ensure all required files are available.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
