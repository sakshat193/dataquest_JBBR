import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load models and transformers
with open("Notebooks/Models/best_xgb_model.pkl", "rb") as file:
    model = pickle.load(file)
with open("Notebooks/Models/scaler.pkl", "rb") as file:
    scaler = pickle.load(file)
with open("Notebooks/Models/label_encoder.pkl", "rb") as file:
    label_encoder = pickle.load(file)

# Get color for prediction
def get_color(alert_status):
    return {
        "Red": "#FFCCCC",     # Light Red
        "Orange": "#FFE6CC",  # Light Orange
        "Yellow": "#FFFFCC",  # Light Yellow
        "Green": "#CCFFCC",   # Light Green
        "No Alert": "#FFFFFF" # White for no alert
    }.get(alert_status, "#FFFFFF")  # Default White

# Add custom CSS
def add_custom_css():
    st.markdown("""
        <style>
        .home-button {
            margin: 20px 0;
            width: 120px;
            text-align: center;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .home-button:hover {
            background-color: #45a049;
        }

        .prediction-box {
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

# Alert Prediction Page
def alert_prediction():
    # Add custom CSS
    add_custom_css()
    
    # Add a Streamlit button for Home navigation
    if st.button("🏠 Home", key="home_button", help="Return to the Home page"):
        st.session_state.current_page = "Home"
        st.rerun()
    
    st.title("Earthquake Alert Prediction")
    st.markdown("Enter the required features below to predict the alert status.")

    # User inputs
    dmin = st.number_input("Minimum Distance to Epicenter (dmin)", min_value=0.0)
    sig = st.number_input("Significance (sig)", min_value=0)
    magnitude = st.number_input("Magnitude", min_value=0.0)
    tsunami = st.selectbox("Tsunami Warning", ["No", "Yes"], help="Select 'Yes' for 1 and 'No' for 0")
    depth = st.number_input("Depth (km)", min_value=0.0)

    tsunami = 1 if tsunami == "Yes" else 0

    # Prediction button
    if st.button("Predict Alert"):
        # Prepare input data
        input_data = pd.DataFrame([[dmin, sig, magnitude, tsunami, depth]],
                                  columns=["dmin", "sig", "magnitude", "tsunami", "depth"])
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)

        alert_status = label_encoder.inverse_transform(prediction)[0]

        if alert_status == 'green':
            alert_status = 'Green'

        if alert_status == 'red':
            alert_status = 'Red'
            
        if alert_status == 'yellow':
            alert_status = 'Yellow'
            
        if alert_status == 'orange':
            alert_status = 'Orange'
            
        if alert_status == 'no alert':
            alert_status = 'No alert'

        # Get color and set text color for prediction
        color = get_color(alert_status)
        text_color = "black" if alert_status == "No Alert" else "red" if alert_status == "red" else \
                     "orange" if alert_status == "orange" else "yellow" if alert_status == "yellow" else "green"

        # Display prediction with color-coded box and text
        st.markdown(f"""
            <div class="prediction-box" style="background-color: {color}; color: {text_color};">
                Predicted Alert Status: <strong>{alert_status}</strong>
            </div>
        """, unsafe_allow_html=True)

# Call the alert prediction function
alert_prediction()
