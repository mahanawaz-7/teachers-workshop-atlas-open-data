import streamlit as st
from utils import load_markdown_file_with_images, get_first_level_headers, load_markdown_preview, start_done_buttons

def run(selected_tab=None):
    folder = "foundations"

    # Initialize session state for expanded state of sections
    if "expanded_intro" not in st.session_state:
        st.session_state["expanded_intro"] = False
    if "expanded_standard_model" not in st.session_state:
        st.session_state["expanded_standard_model"] = False
    if "expanded_higgs" not in st.session_state:
        st.session_state["expanded_higgs"] = False
    if "expanded_unknown" not in st.session_state:
        st.session_state["expanded_unknown"] = False

    # Get the selected language from session state
    selected_language = st.session_state.get("language", "english").lower()

    # Get the intro to the module
    general_info = '00_intro.md'
    # Create paths and titles for each section
    tabs_path = ['01_particles.md', '02_standard_model.md', '03_higgs.md', '04_unknown.md']
    tab_titles = get_first_level_headers(selected_language, folder, tabs_path)

    # Print the intro to the module
    load_markdown_file_with_images(general_info, folder, selected_language)

    # Load previews (first few lines of the markdown files)
    intro_preview = load_markdown_preview(tabs_path[0], folder, selected_language, lines=3)
    standard_model_preview = load_markdown_preview(tabs_path[1], folder, selected_language, lines=3)
    higgs_preview = load_markdown_preview(tabs_path[2], folder, selected_language, lines=3)
    uknown_preview = load_markdown_preview(tabs_path[3], folder, selected_language, lines=3)

    # Create the tabs
    tabs = st.tabs(tab_titles)
    # Get the start/done buttons
    start, done = start_done_buttons(selected_language)

    # Tab 1: What are particles
    with tabs[0]:
        if not st.session_state["expanded_intro"]:
            # Show preview
            preview_lines = intro_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button(start, key="intro_read"):
                st.session_state["expanded_intro"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_with_images(tabs_path[0], folder, selected_language)
            if st.button(done, key="intro_done"):
                st.session_state["expanded_intro"] = False
                st.rerun()  # Refresh the app to show the preview again

    # Tab 2: The standard model
    with tabs[1]:
        if not st.session_state["expanded_standard_model"]:
            # Show preview
            preview_lines = standard_model_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button(start, key="standard_model_read"):
                st.session_state["expanded_standard_model"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_with_images(tabs_path[1], folder, selected_language)
            if st.button(done, key="standard_model_done"):
                st.session_state["expanded_standard_model"] = False
                st.rerun()  # Refresh the app to show the preview again

    # Tab 3: The Higgs boson
    with tabs[2]:
        if not st.session_state["expanded_higgs"]:
            # Show preview
            preview_lines = higgs_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button(start, key="higgs_read"):
                st.session_state["expanded_higgs"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_with_images(tabs_path[2], folder, selected_language)
            if st.button(done, key="higgs_done"):
                st.session_state["expanded_higgs"] = False
                st.rerun()  # Refresh the app to show the preview again


    # Tab 4: The Unknown
    with tabs[3]:
        if not st.session_state["expanded_unknown"]:
            # Show preview
            preview_lines = uknown_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button(start, key="unknown_read"):
                st.session_state["expanded_unknown"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_with_images(tabs_path[3], folder, selected_language)
            if st.button(done, key="unknown_done"):
                st.session_state["expanded_unknown"] = False
                st.rerun()  # Refresh the app to show the preview again