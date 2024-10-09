import streamlit as st
import io
import sys
import json
from utils import load_markdown_file_with_images_and_code, get_first_level_headers, load_markdown_preview, load_markdown_file_with_images

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
    general_info = '00_before_class.md'
    tabs_path = ['01_intro.md', '02_histograms.md']
    tab_titles = get_first_level_headers(selected_language, folder, tabs_path)

    load_markdown_file_with_images(general_info, folder, selected_language)
     
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
