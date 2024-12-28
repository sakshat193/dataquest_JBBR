import streamlit as st
import streamlit.components.v1 as components

# Embed the Power BI iframe (replace with your embed URL)
power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiYWEzY2U0OGItYjJiYi00ZjAzLWIyNDAtN2MwYzZlZmU2YTdkIiwidCI6ImQxZjE0MzQ4LWYxYjUtNGEwOS1hYzk5LTdlYmYyMTNjYmM4MSIsImMiOjEwfQ%3D%3D"
st.title("Streamlit Web App with Power BI Dashboard")

# Embed Power BI Report
components.iframe(power_bi_url, width=900, height=600)

# Additional Streamlit content
st.write("This is a web app embedding a Power BI report.")

