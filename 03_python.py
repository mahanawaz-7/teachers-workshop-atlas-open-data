# # import streamlit as st
# # import io
# # import sys
# # import json
# # from utils import load_markdown_file_with_images_and_code,get_first_level_headers

# # # Define backend variables and functions that will be available to the user's code

# # selected_language = st.session_state.get("language", "english").lower()

# # def run(selected_tab=None):
# #     global_namespace = {}
# #     #load_markdown_file_with_images_and_code('01_intro.md', 'python', global_namespace, selected_language)

# #     folder = "python"
# #     # Initialize session state for selected tab
# #     if "selected_tab" not in st.session_state:
# #         st.session_state["selected_tab"] = selected_tab

# #     # Get the selected language from session state
# #     selected_language = st.session_state.get("language", "english").lower()
# #     # Create tabs for each section
# #     tabs_path = ['01_intro.md', '02_histograms.md']
# #     tab_titles = get_first_level_headers(selected_language, folder, tabs_path)
# #     tabs = st.tabs(tab_titles)

# #     # Map tab titles to tab objects
# #     tab_dict = dict(zip(tab_titles, tabs))

# #     # Display content based on selected tab
# #     for tab_title in tab_titles:
# #         with tab_dict[tab_title]:
# #             # Update the session state when the tab is selected
# #             if tab_title != st.session_state["selected_tab"]:
# #                 st.session_state["selected_tab"] = tab_title
# #             if tab_title == tab_titles[0]:
# #                 # Pass the selected language to the function
# #                 load_markdown_file_with_images_and_code(tabs_path[0], folder, global_namespace, selected_language)
# #             elif tab_title == tab_titles[1]:
# #                 # Pass the selected language to the function
# #                 load_markdown_file_with_images_and_code(tabs_path[1], folder, global_namespace, selected_language)

# import streamlit as st
# import io
# import sys
# import json
# from utils import load_markdown_file_with_images_and_code, get_first_level_headers

# # Define backend variables and functions that will be available to the user's code
# selected_language = st.session_state.get("language", "english").lower()

# def run(selected_tab=None):
#     # Shared global namespace across all cells
#     global_namespace = {}

#     # Folder where markdown files are stored
#     folder = "python"

#     # Initialize session state for selected tab
#     if "selected_tab" not in st.session_state:
#         st.session_state["selected_tab"] = selected_tab

#     # Create tabs for each section
#     tabs_path = ['01_intro.md', '02_histograms.md']  # List of markdown file names
#     tab_titles = get_first_level_headers(selected_language, folder, tabs_path)  # Get tab titles from the headers of markdown files
#     tabs = st.tabs(tab_titles)

#     # Map tab titles to their corresponding tab objects
#     tab_dict = dict(zip(tab_titles, tabs))

#     # Display content based on selected tab
#     for tab_title in tab_titles:
#         with tab_dict[tab_title]:
#             # Update the session state when the tab is selected
#             if tab_title != st.session_state["selected_tab"]:
#                 st.session_state["selected_tab"] = tab_title

#             # Load the appropriate markdown file based on the selected tab
#             if tab_title == tab_titles[0]:
#                 load_markdown_file_with_images_and_code(tabs_path[0], folder, global_namespace, selected_language)
#             elif tab_title == tab_titles[1]:
#                 load_markdown_file_with_images_and_code(tabs_path[1], folder, global_namespace, selected_language)

import streamlit as st
import io
import sys
import json
from utils import load_markdown_file_with_images_and_code, get_first_level_headers, load_markdown_preview

# Define backend variables and functions that will be available to the user's code
selected_language = st.session_state.get("language", "english").lower()

def run(selected_tab=None):
    # Shared global namespace across all cells
    global_namespace = {}

    # Folder where markdown files are stored
    folder = "python"

    # Initialize session state for expanded state of sections
    if "expanded_intro" not in st.session_state:
        st.session_state["expanded_intro"] = False
    if "expanded_histograms" not in st.session_state:
        st.session_state["expanded_histograms"] = False

    # Create paths and titles for each section
    tabs_path = ['01_intro.md', '02_histograms.md']
    tab_titles = get_first_level_headers(selected_language, folder, tabs_path)

    st.title("Introduction to coding in Python")
    st.markdown("Some info about the thing that they will do here.")
     
    # Create the tabs
    tabs = st.tabs(tab_titles)

    # Tab 1: Introduction
    with tabs[0]:
        # Load preview for intro
        intro_preview = load_markdown_preview(tabs_path[0], folder, selected_language, lines=3)

        if not st.session_state["expanded_intro"]:
            # Show preview
            preview_lines = intro_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button("Read more", key="intro_read"):
                st.session_state["expanded_intro"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_with_images_and_code(tabs_path[0], folder, global_namespace, selected_language)
            if st.button("Done!", key="intro_done"):
                st.session_state["expanded_intro"] = False
                st.rerun()  # Refresh the app to show the preview again

    # Tab 2: Histograms
    with tabs[1]:
        # Load preview for histograms
        histograms_preview = load_markdown_preview(tabs_path[1], folder, selected_language, lines=3)

        if not st.session_state["expanded_histograms"]:
            # Show preview
            preview_lines = histograms_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button("Read more", key="histograms_read"):
                st.session_state["expanded_histograms"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_with_images_and_code(tabs_path[1], folder, global_namespace, selected_language)
            if st.button("Done!", key="histograms_done"):
                st.session_state["expanded_histograms"] = False
                st.rerun()  # Refresh the app to show the preview again
