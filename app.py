import streamlit as st
from streamlit_option_menu import option_menu
import importlib
from utils import load_sidebar_tabs

# Initialize session state for language selection
if "language_selected" not in st.session_state:
    st.session_state["language_selected"] = False

if "language" not in st.session_state:
    st.session_state["language"] = None

# Initialize session state for selected tab
if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = None

# Define a callback function to set session state when "Proceed" button is clicked
def proceed(language):
    st.session_state["language_selected"] = True
    st.session_state["language"] = language

# Define a callback function to reset the language selection (for the "Change Language" button)
def reset_language():
    st.session_state["language_selected"] = False
    st.session_state["language"] = None

# Main page (landing page with language selection)
if not st.session_state["language_selected"]:
    st.title("Welcome to the ATLAS Open Data Teachers Workshop")
    
    st.write("Please select your language to continue:")
    
    # Dropdown for language selection
    language = st.selectbox("Select Language", ["English", "Spanish"])
    
    # Proceed button with a callback function
    st.button("Proceed", on_click=proceed, args=(language,))

# # Check if English is selected
# elif st.session_state["language"] == "English":
else:
    st.sidebar.title("ATLAS Open Data Teachers Workshop")
    sidebar_top = st.sidebar.container()  # Create a container for the top part of the sidebar
    sidebar_bottom = st.sidebar.container()  # Create a container for the bottom part of the sidebar
    # Use the top container for the main menu
    with sidebar_top:
        tabs = load_sidebar_tabs(st.session_state['language'])
        selected_tab = option_menu(
            "",
            tabs,
            menu_icon="code",  # Customize menu icon (optional)
            default_index=0,
        )

    # Check if the selected tab has changed
    if st.session_state["selected_tab"] != selected_tab:
        st.session_state["selected_tab"] = selected_tab

    # Dynamically import and display the content of the selected tab
    if selected_tab == tabs[0]:
        module = importlib.import_module("00_welcome")
        module.run(selected_tab)

    elif selected_tab == tabs[1]:
        module = importlib.import_module("03_python")
        module.run(selected_tab)

    elif selected_tab == tabs[2]:
        module = importlib.import_module("01_foundations")
        module.run(selected_tab)

    elif selected_tab == tabs[3]:
        module = importlib.import_module("02_experimental")
        module.run(selected_tab)

    elif selected_tab == tabs[4]:
        module = importlib.import_module("04_analyses")
        module.run(selected_tab)

    # Use the bottom container to place the language section at the bottom
    with sidebar_bottom:
        st.sidebar.markdown("<br><br><br><br><br>", unsafe_allow_html=True)  # Add some space
        st.sidebar.text(f"Language: {st.session_state['language']}")
        st.sidebar.button("Change Language", on_click=reset_language)
