import streamlit as st
from utils import load_markdown_file_with_images, get_first_level_headers, load_markdown_preview

def run(selected_tab=None):
    folder = "foundations"

    # Initialize session state for expanded state of sections
    if "expanded_intro" not in st.session_state:
        st.session_state["expanded_intro"] = False
    if "expanded_standard_model" not in st.session_state:
        st.session_state["expanded_standard_model"] = False
    if "expanded_unknown" not in st.session_state:
        st.session_state["expanded_unknown"] = False

    # Get the selected language from session state
    selected_language = st.session_state.get("language", "english").lower()

    # Create paths and titles for each section
    general_info = '00_intro.md'
    tabs_path = ['01_fermions.md', '02_bosons.md', '03_unknown.md']
    tab_titles = get_first_level_headers(selected_language, folder, tabs_path)

    load_markdown_file_with_images(general_info, folder, selected_language)

    # Load previews (first few lines of the markdown files)
    intro_preview = load_markdown_preview(tabs_path[0], folder, selected_language, lines=3)
    standard_model_preview = load_markdown_preview(tabs_path[1], folder, selected_language, lines=3)
    uknown_preview = load_markdown_preview(tabs_path[2], folder, selected_language, lines=3)

    # Create the tabs
    tabs = st.tabs(tab_titles)

    # Tab 1: Fermions
    with tabs[0]:
        if not st.session_state["expanded_intro"]:
            # Show preview
            preview_lines = intro_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button("Start!", key="intro_read"):
                st.session_state["expanded_intro"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_with_images(tabs_path[0], folder, selected_language)
            if st.button("Done!", key="intro_done"):
                st.session_state["expanded_intro"] = False
                st.rerun()  # Refresh the app to show the preview again

    # Tab 2: Bosons
    with tabs[1]:
        if not st.session_state["expanded_standard_model"]:
            # Show preview
            preview_lines = standard_model_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button("Start!", key="standard_model_read"):
                st.session_state["expanded_standard_model"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_with_images(tabs_path[1], folder, selected_language)
            if st.button("Done!", key="standard_model_done"):
                st.session_state["expanded_standard_model"] = False
                st.rerun()  # Refresh the app to show the preview again

    # Tab 3: The Unknown
    with tabs[2]:
        if not st.session_state["expanded_unknown"]:
            # Show preview
            preview_lines = uknown_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button("Start!", key="unknown_read"):
                st.session_state["expanded_unknown"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_with_images(tabs_path[2], folder, selected_language)
            if st.button("Done!", key="unknown_done"):
                st.session_state["expanded_unknown"] = False
                st.rerun()  # Refresh the app to show the preview again
