import streamlit as st
import pandas as pd
import pickle
import numpy as np
try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
except ImportError:
    st.error("Please install geopy using: pip install geopy --user")
    st.stop()
import time


def load_models(base_path="Notebooks/Predictions_Training/Models/"):
    """Load all required models and transformers"""
    try:
        # Load the model and transformers
        with open(f"{base_path}best_rfc_model.pkl", 'rb') as f:
            model = pickle.load(f)
        with open(f"{base_path}scaler.pkl", 'rb') as f:
            scaler = pickle.load(f)
        with open(f"{base_path}top_6_features.pkl", 'rb') as f:
            top_6_features = pickle.load(f)
        return model, scaler, top_6_features
    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.stop()


def get_location_from_coords(latitude, longitude, max_retries=3):
    """Get location name from coordinates with retry mechanism and extended error handling"""
    geolocator = Nominatim(user_agent="app")
    
    for attempt in range(max_retries):
        try:
            st.info(f"Attempt {attempt+1}: Fetching location for coordinates ({latitude}, {longitude})...")
            coords = f"{latitude}, {longitude}"
            location = geolocator.reverse(coords, language='en', timeout=20)
            
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
                return f"{state}, {country}".strip(', '), True
            
            time.sleep(1)  # Wait between retries
            
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            if attempt == max_retries - 1:
                st.warning(f"Location service is temporarily unavailable. Attempt {attempt+1} failed: {e}")
                return f"Coordinates: ({latitude:.4f}, {longitude:.4f})", False
            time.sleep(2)  # Wait longer between retries
            
        except Exception as e:
            st.error(f"Unexpected error occurred: {e}")
            return f"Coordinates: ({latitude:.4f}, {longitude:.4f})", False
    
    return f"Coordinates: ({latitude:.4f}, {longitude:.4f})", False


def significance_prediction():
    st.title("Earthquake Significance Prediction")
    
    try:
        # Load models and preprocessing tools
        model, scaler, top_6_features = load_models()
        
        # Create input form
        with st.form("significance_prediction_form"):
            # Alert selection
            alert_options = ['No alert', 'green', 'yellow', 'orange', 'red']
            alert = st.selectbox("Select Alert Level", alert_options)
            
            # Magnitude slider
            magnitude = st.slider("Magnitude", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
            
            # Coordinates input
            col1, col2 = st.columns(2)
            with col1:
                latitude = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=0.0)
            with col2:
                longitude = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=0.0)
            
            # Display location immediately after coordinates input
            if latitude != 0.0 or longitude != 0.0:  # Only show if coordinates are changed
                with st.spinner("Detecting location..."):
                    detected_location, success = get_location_from_coords(latitude, longitude)
                    
                    # Different styling based on whether location service worked
                    border_color = "#4CAF50" if success else "#FFA500"
                    icon = "📍" if success else "⚠️"
                    
                    st.markdown("### Location Information")
                    st.markdown(f"""
                    <div style='padding: 10px; border-radius: 5px; border: 1px solid {border_color}; background-color: #f8f9fa;'>
                        {icon} <b>{detected_location}</b>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Submit button
            if st.form_submit_button("Predict Significance"):
                # Encode alert as a numerical value
                alert_mapping = {"No alert": 0, "green": 1, "yellow": 2, "orange": 3, "red": 4}
                encoded_alert = alert_mapping.get(alert, 0)
                
                # Prepare input data
                input_data = pd.DataFrame({
                    'alert': [encoded_alert],
                    'magnitude': [magnitude],
                    'longitude': [longitude],
                    'latitude': [latitude]
                })
                
                # Transform features using the loaded scaler
                transformed_data = input_data.copy()
                transformed_data[['longitude', 'latitude']] = scaler.transform(input_data[['longitude', 'latitude']])

                # Select only the top 6 features for the model
                transformed_data_top_6 = transformed_data.iloc[:, top_6_features]
                
                # Make prediction using the trained model
                try:
                    significance = model.predict(transformed_data_top_6)[0]
                    significance_prob = model.predict_proba(transformed_data_top_6)[0]
                    
                    # Display results
                    st.success(f"Predicted Significance: {significance}")
                    
                    # Display probability distribution
                    st.write("Probability Distribution:")
                    prob_df = pd.DataFrame({
                        'Significance Level': model.classes_,
                        'Probability': significance_prob
                    })
                    st.bar_chart(prob_df.set_index('Significance Level'))
                    
                    # Additional information
                    st.write("### Interpretation Guide:")
                    st.write("- Significance < 100: Minor impact")
                    st.write("- Significance 100-500: Moderate impact")
                    st.write("- Significance 500-1000: Major impact")
                    st.write("- Significance > 1000: Severe impact")
                except Exception as e:
                    st.error(f"Prediction error: {e}")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.write("Please ensure all model files are in the correct location and the input values are valid.")


if __name__ == "__main__":
    significance_prediction()
