import streamlit as st
from pathlib import Path

# Load pages dynamically
def load_page(page: str):
    with open(f"pages/{page}.py") as f:
        exec(f.read(), {"st": st})

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Predictive Models 1", "Predictive Models 2", "Geospatial Map 1", "Geospatial Map 2", "Dashboard"],
)

# Load the selected page
pages = {
    "Home": "home",
    "Predictive Models 1": "predictive_1",
    "Predictive Models 2": "predictive_2",
    "Geospatial Map 1": "geospatial_1",
    "Geospatial Map 2": "geospatial_2",
    "Dashboard": "dashboard",
}
load_page(pages[page])
