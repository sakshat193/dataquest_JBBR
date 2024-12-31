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

        .feature-info {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
            border-left: 3px solid #4CAF50;
        }
        </style>
    """, unsafe_allow_html=True)

# Feature explanations
FEATURE_INFO = {
    "dmin": """
    **Minimum Distance to Epicenter (dmin)**
    
    This is the shortest distance from a seismic monitoring station to the earthquake's epicenter.
    - Measured in degrees (°) of arc on Earth's surface
    - Smaller values mean the station is closer to the epicenter
    - Important for determining the accuracy of magnitude estimates
    - Typical range: 0° to 180°
    """,
    
    "sig": """
    **Significance of the Earthquake**
    
    A number that describes the relative significance of the earthquake.
    - Calculated from magnitude and felt reports
    - Higher values indicate more significant events
    - Considers factors like:
        * Population exposure
        * Potential damage
        * Media attention
    - Typical range: 0 to 1000
    """,
    
    "magnitude": """
    **Earthquake Magnitude**
    
    The amount of energy released by the earthquake.
    - Measured on the Richter scale or Moment magnitude scale
    - Logarithmic scale: each point increase = 10x more energy
    - General impact levels:
        * < 3.0: Usually not felt
        * 3.0-4.9: Often felt, minor damage
        * 5.0-6.9: Can cause significant damage
        * 7.0+: Major earthquake, severe damage
    """,
    
    "tsunami": """
    **Tsunami Warning**
    
    Indicates whether the earthquake has triggered a tsunami warning.
    - Yes (1): Potential for tsunami generation
    - No (0): No tsunami threat
    
    Factors considered:
    - Earthquake depth
    - Magnitude
    - Location (underwater or coastal)
    - Plate movement type
    """,
    
    "depth": """
    **Earthquake Depth**
    
    The depth below Earth's surface where the earthquake originated.
    - Measured in kilometers (km)
    - Classifications:
        * Shallow: 0-70 km
        * Intermediate: 70-300 km
        * Deep: 300-700 km
    - Shallow earthquakes typically cause more surface damage
    """
}

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

    # User inputs with expandable information
    with st.expander("ℹ️ What is Minimum Distance to Epicenter?"):
        st.markdown(FEATURE_INFO["dmin"])
    dmin = st.number_input("Minimum Distance to Epicenter (dmin)", min_value=0.0)
    
    with st.expander("ℹ️ What is Earthquake Significance?"):
        st.markdown(FEATURE_INFO["sig"])
    sig = st.number_input("Significance of the Earthquake", min_value=0)
    
    with st.expander("ℹ️ What is Earthquake Magnitude?"):
        st.markdown(FEATURE_INFO["magnitude"])
    magnitude = st.slider("Magnitude", min_value=0.0, max_value=10.0, step=0.1, value=5.0)
    
    with st.expander("ℹ️ What is a Tsunami Warning?"):
        st.markdown(FEATURE_INFO["tsunami"])
    tsunami = st.selectbox("Tsunami Warning", ["No", "Yes"])
    
    with st.expander("ℹ️ What is Earthquake Depth?"):
        st.markdown(FEATURE_INFO["depth"])
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
            alert_status = 'No Alert'

        # Get color and set text color for prediction
        color = get_color(alert_status)
        text_color = "black" if alert_status == "No alert" else "red" if alert_status == "Red" else \
                     "orange" if alert_status == "Orange" else "yellow" if alert_status == "Yellow" else "green"

        # Display prediction with color-coded box and text
        st.markdown(f"""
            <div class="prediction-box" style="background-color: {color}; color: {text_color};">
                Predicted Alert Status: <strong>{alert_status}</strong>
            </div>
        """, unsafe_allow_html=True)

# Call the alert prediction function
alert_prediction()