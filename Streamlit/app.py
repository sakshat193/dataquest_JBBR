import streamlit as st
from pages.alert_prediction import alert_prediction
from pages.power_bi_dashboard import power_bi_dashboard
from pages.significance import significance
# Custom CSS for glowing button effect
def add_custom_css():
    st.markdown("""
        <style>
        .nav-button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 2px solid #4CAF50;
            border-radius: 5px;
            background-color: transparent;
            color: #4CAF50;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .nav-button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px #4CAF50;
            background-color: #4CAF50;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# Home Page
def home():
    st.title("Earthquake Alert Prediction System")
    st.markdown("""
    Welcome to the Earthquake Alert Prediction System. 
    Choose an option below to proceed:
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Alert Prediction", key="alert"):
            st.session_state.current_page = "Alert Prediction"
            st.rerun()
    with col2:
        if st.button("Power BI Dashboard", key="dashboard"):
            st.session_state.current_page = "Power BI Dashboard"
            st.rerun()
    with col3:
        if st.button("Significance", key="significance"):
            st.session_state.current_page = "Significance"
            st.rerun()

# Main App
def main():
    add_custom_css()

    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

    # Navigate to the selected page
    if st.session_state.current_page == "Home":
        home()
    elif st.session_state.current_page == "Alert Prediction":
        alert_prediction()
    elif st.session_state.current_page == "Power BI Dashboard":
        power_bi_dashboard()
    elif st.session_state.current_page == "Significance":
        significance()

if __name__ == "__main__":
    main()
