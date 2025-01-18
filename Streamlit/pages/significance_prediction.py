import streamlit as st
import pickle
import numpy as np
import os

# Base path to models
MODEL_BASE_PATH = "Notebooks/Predictions_Training/Models/"

# Load the pre-trained model and scaler
with open(os.path.join(MODEL_BASE_PATH, "best_rfc_model.pkl"), "rb") as model_file:
    best_rfc_model = pickle.load(model_file)

with open(os.path.join(MODEL_BASE_PATH, "scaler.pkl"), "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

# Significance Prediction Page
def significance_prediction():
    st.title("Earthquake Significance Prediction")

    # Define the input fields directly
    st.write("Provide the input values for the model:")

    magnitude = st.slider("Magnitude", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
    mmi = st.slider("MMI", min_value=1, max_value=10, value=6, step=1)  # MMI starts from 1
    cdi = st.slider("CDI", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
    alert_options = {"No alert": 0, "Green": 1, "Yellow": 2, "Orange": 3, "Red": 4}
    alert = st.selectbox("Alert Level", list(alert_options.keys()))
    latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=0.0)
    longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=0.0)

    # Encode the alert input
    encoded_alert = alert_options[alert]

    # Predict button
    if st.button("Predict Significance"):
        # Prepare the input data
        input_data = np.array([magnitude, mmi, cdi, encoded_alert, latitude, longitude]).reshape(1, -1)
        
        # Scale the input data
        input_data_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = best_rfc_model.predict(input_data_scaled)
        st.success(f"The predicted significance is: {prediction[0]:.2f}")

    # Home navigation button
    if st.button("\U0001F3E0 Home", key="home_button", help="Return to the Home page"):
        st.session_state.current_page = "Home"
        st.rerun()
