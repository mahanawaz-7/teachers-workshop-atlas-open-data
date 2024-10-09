import streamlit as st
from utils import load_markdown_file_with_images, get_first_level_headers, load_markdown_preview

def run(selected_tab=None):
    folder = "experimental"

    # Initialize session state for expanded state of sections
    if "expanded_accelerators" not in st.session_state:
        st.session_state["expanded_accelerators"] = False
    if "expanded_detectors" not in st.session_state:
        st.session_state["expanded_detectors"] = False

    # Get the selected language from session state
    selected_language = st.session_state.get("language", "english").lower()

    # Create paths and titles for each section
    tabs_path = ['01_accelerators.md', '02_detectors.md']
    tab_titles = get_first_level_headers(selected_language, folder, tabs_path)

    st.title("Detectors")
    st.markdown("Some info about the thing that they will do here.")

    # Create the tabs
    tabs = st.tabs(tab_titles)

    # Tab 1: Accelerators
    with tabs[0]:
        # Load preview for accelerators
        accelerators_preview = load_markdown_preview(tabs_path[0], folder, selected_language, lines=3)

        if not st.session_state["expanded_accelerators"]:
            # Show preview
            preview_lines = accelerators_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button("Read more", key="accelerators_read"):
                st.session_state["expanded_accelerators"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content and video
            load_markdown_file_with_images(tabs_path[0], folder, selected_language)
            st.video("https://www.youtube.com/embed/pQhbhpU9Wrg")
            if st.button("Done!", key="accelerators_done"):
                st.session_state["expanded_accelerators"] = False
                st.rerun()  # Refresh the app to show the preview again

    # Tab 2: Detectors
    with tabs[1]:
        # Load preview for detectors
        detectors_preview = load_markdown_preview(tabs_path[1], folder, selected_language, lines=3)

        if not st.session_state["expanded_detectors"]:
            # Show preview
            preview_lines = detectors_preview.splitlines()
            st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
            st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
            if st.button("Read more", key="detectors_read"):
                st.session_state["expanded_detectors"] = True
                st.rerun()  # Refresh the app to display the full content
        else:
            # Show full content
            load_markdown_file_with_images(tabs_path[1], folder, selected_language)
            if st.button("Done!", key="detectors_done"):
                st.session_state["expanded_detectors"] = False
                st.rerun()  # Refresh the app to show the preview again
