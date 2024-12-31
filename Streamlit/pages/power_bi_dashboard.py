import streamlit as st

def add_dashboard_css():
    st.markdown("""
        <style>
        .home-button {
            position: fixed;
            top: 10px;
            left: 10px;
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            z-index: 999;
            transition: all 0.3s ease;
        }
        
        .home-button:hover {
            background-color: #45a049;
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
            transform: scale(1.05);
        }

        .dashboard-container {
            width: 100%; /* Set the dashboard width to 100% */
            max-width: 1200px; /* Max width to avoid being too wide */
            height: 800px;
            margin: 20px auto; /* Centered the container horizontally */
            border: none;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        iframe {
            width: 100%;
            height: 100%;
            border: none;
            border-radius: 8px;
        }

        .link-container {
            text-align: center;
            margin-top: 30px;
        }

        .link-container a {
            color: #0073e6;
            font-size: 16px;
            text-decoration: none;
            margin: 10px 15px;
            padding: 8px 16px;
            border: 2px solid #0073e6;
            border-radius: 5px;
            transition: all 0.3s ease;
        }

        .link-container a:hover {
            background-color: #0073e6;
            color: white;
            box-shadow: 0 0 8px rgba(0, 115, 230, 0.5);
        }
        </style>
    """, unsafe_allow_html=True)

# Power BI Dashboard Page
def power_bi_dashboard():
    # Add custom CSS
    add_dashboard_css()

    # Add home button using Streamlit button
    if st.button("🏠 Home"):
        st.session_state.current_page = "Home"
        st.rerun()

    # Add some spacing after the home button
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.title("Power BI Dashboards and Maps")

    # Embed the first Power BI Dashboard
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNmUwZmE5MTgtNTliNC00MjAwLWE3MTItZGNiNmU3YzgzZTZhIiwidCI6ImQxZjE0MzQ4LWYxYjUtNGEwOS1hYzk5LTdlYmYyMTNjYmM4MSIsImMiOjEwfQ%3D%3D"
    
    # Embed using HTML iframe with responsive container and fixed width
    st.markdown(f"""
        <div class="dashboard-container">
            <iframe src="{powerbi_url}"
                    allowFullScreen={True}>
            </iframe>
        </div>
    """, unsafe_allow_html=True)

    # Add a direct link below the dashboard
    st.markdown("""
        <div style="margin-top: 20px; text-align: center;">
            <p>If the dashboard doesn't load properly, you can 
               <a href="https://app.powerbi.com/view?r=eyJrIjoiNmUwZmE5MTgtNTliNC00MjAwLWE3MTItZGNiNmU3YzgzZTZhIiwidCI6ImQxZjE0MzQ4LWYxYjUtNGEwOS1hYzk5LTdlYmYyMTNjYmM4MSIsImMiOjEwfQ%3D%3D" 
                  target="_blank">open it in a new window</a>.</p>
        </div>
    """, unsafe_allow_html=True)

    # Add new Power BI links below
    st.markdown("""
        <div class="link-container">
            <a href="https://app.powerbi.com/view?r=eyJrIjoiYjZmNGFjMzUtNTBhNy00MGQ0LTljZjItY2ZhNmM1M2E3OWEwIiwidCI6ImQxZjE0MzQ4LWYxYjUtNGEwOS1hYzk5LTdlYmYyMTNjYmM4MSIsImMiOjEwfQ%3D%3D" target="_blank">
                Open Seismic Activity Map
            </a>
            <a href="https://app.powerbi.com/view?r=eyJrIjoiNjcxYThkZjEtY2NkZC00MmFhLTlmYzMtMDNiZDJlYmM0ZDE5IiwidCI6ImQxZjE0MzQ4LWYxYjUtNGEwOS1hYzk5LTdlYmYyMTNjYmM4MSIsImMiOjEwfQ%3D%3D" target="_blank">
                Open Tsunami Risk Map
            </a>
        </div>
    """, unsafe_allow_html=True)

# Home Page (Placeholder for Home)
def home_page():
    st.title("Welcome to the Home Page!")
    st.write("This is the home page. You can add more content or functionality here.")

# Main function to handle the app logic
def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"  # Set default page
    
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "power_bi_dashboard":
        power_bi_dashboard()

if __name__ == "__main__":
    main()
