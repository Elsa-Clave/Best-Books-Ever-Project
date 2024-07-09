import streamlit as st
from streamlit_option_menu import option_menu


# Import your page scripts
import recommender
import tableau_dashboard
from PIL import Image

# Set page configuration
st.set_page_config(page_title="BESTBOOKSEVER", page_icon=":book:", layout="wide")

# Set up the navigation menu
with st.sidebar:
    selected = option_menu(
        menu_title="More stuff",
        options=["Book Recommender", "Tableau Dashboard"],
        icons=["book", "table"],
        menu_icon="cast",
        default_index=0,
    )

# Display the selected page
if selected == "Book Recommender":
    recommender.show_recommender()
elif selected == "Tableau Dashboard":
    tableau_dashboard.show_dashboard()
    