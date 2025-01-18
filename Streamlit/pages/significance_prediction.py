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

# Add custom CSS for home button positioning
def add_custom_css():
    st.markdown("""
        <style>
        .home-button {
            position: absolute;
            top: 10px;
            left: 10px;
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
    "cdi": """
    **Community Internet Intensity Map (CDI)**

    CDI measures the intensity of shaking felt and reported by people.
    - Range: 0.0 to 10.0
    - Higher values indicate stronger perceived shaking.
    - CDI is based on community surveys and reports.
    """,

    "mmi": """
    **Modified Mercalli Intensity Scale (MMI)**

    MMI quantifies the impact of an earthquake on people, buildings, and the Earth's surface.
    - Scale: 1 (Not Felt) to 10 (Extreme)
    - Definitions:
        * **1**: Not felt except by a very few under especially favorable conditions.
        * **2**: Felt only by a few persons at rest, especially on upper floors of buildings.
        * **3**: Felt quite noticeably by persons indoors, especially on upper floors. Many do not recognize it as an earthquake.
        * **4**: Felt indoors by many, outdoors by few during the day. Dishes, windows, doors disturbed.
        * **5**: Felt by nearly everyone; many awakened. Some dishes, windows broken. Unstable objects overturned.
        * **6**: Felt by all; many frightened. Some heavy furniture moved; some instances of fallen plaster.
        * **7**: Damage negligible in buildings of good design and construction; slight to moderate in well-built ordinary structures; considerable damage in poorly built or badly designed structures.
        * **8**: Damage slight in specially designed structures; considerable damage in ordinary substantial buildings with partial collapse. Damage great in poorly built structures.
        * **9**: Damage considerable in specially designed structures; buildings shifted off foundations. Ground cracked.
        * **10**: Some well-built wooden structures destroyed; most masonry and frame structures destroyed with foundations. Ground badly cracked. Landslides considerable.
    """
}

# Significance Prediction Page
def significance_prediction():
    # Add custom CSS
    add_custom_css()

    # Home button at the top-left corner
    if st.button("\U0001F3E0 Home", key="home_button", help="Return to the Home page", args=("home-button",)):
        st.session_state.current_page = "Home"
        st.rerun()

    st.title("Earthquake Significance Prediction")

    # Define the input fields with information dropdowns
    st.markdown("Enter the required features below to predict earthquake significance.")

    magnitude = st.slider("Magnitude", min_value=0.0, max_value=10.0, value=5.0, step=0.1)

    with st.expander("\u2139\ufe0f What is MMI?"):
        st.markdown(FEATURE_INFO["mmi"])
    mmi = st.slider("MMI", min_value=1, max_value=10, value=6, step=1)

    with st.expander("\u2139\ufe0f What is CDI?"):
        st.markdown(FEATURE_INFO["cdi"])
    cdi = st.slider("CDI", min_value=0.0, max_value=10.0, value=5.0, step=0.1)

    alert_options = {"No alert": 0, "Green": 1, "Yellow": 2, "Orange": 3, "Red": 4}
    alert = st.selectbox("Alert Level", list(alert_options.keys()))

    col1, col2 = st.columns(2)
    with col1:
        latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=0.0)
    with col2:
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

# Call the significance prediction function
significance_prediction()
