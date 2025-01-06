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
        with open(f"{base_path}sig_model.pkl", 'rb') as f:
            model = pickle.load(f)
        with open(f"{base_path}sig_transformers.pkl", 'rb') as f:
            transformers = pickle.load(f)
        with open(f"{base_path}sig_selected_features.pkl", 'rb') as f:
            selected_features = pickle.load(f)
        return model, transformers, selected_features
    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.stop()


def get_location_from_coords(latitude, longitude, max_retries=3):
    """Get location name from coordinates with retry mechanism and extended error handling"""
    geolocator = Nominatim(user_agent="earthquake_app")
    
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
        # Load models
        model, transformers, selected_features = load_models()
        
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
            
            # CDI input
            cdi = st.number_input("Community Decimal Intensity (CDI)", min_value=0.0, max_value=12.0, value=0.0)
            
            # Get location based on coordinates
            if st.form_submit_button("Predict Significance"):
                location, _ = get_location_from_coords(latitude, longitude)
                
                # Prepare input data
                input_data = pd.DataFrame({
                    'alert': [alert],
                    'magnitude': [magnitude],
                    'longitude': [longitude],
                    'latitude': [latitude],
                    'cdi': [cdi],
                    'location': [location]
                })
                
                # Transform features
                transformed_data = input_data.copy()
                for feature, transformer in transformers.items():
                    if feature in input_data.columns:
                        try:
                            transformed_data[feature] = transformer.transform(input_data[feature].values.reshape(-1, 1))
                        except Exception as e:
                            st.warning(f"Error transforming feature '{feature}': {e}")
                
                # Select required features
                X = transformed_data[selected_features]
                
                # Make prediction
                try:
                    significance = model.predict(X)[0]
                    significance_prob = model.predict_proba(X)[0]
                    
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
