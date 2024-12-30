import streamlit as st

st.title("Interactive Dashboard")
st.write("Interact with the dashboard below:")
st.components.v1.iframe("https://powerbi-interactive-dashboard-url", width=800, height=600)
