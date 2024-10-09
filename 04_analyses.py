# import streamlit as st

# import uproot  # for reading .root files
# import awkward as ak  # for handling complex and nested data structures efficiently
# import numpy as np  # for numerical calculations such as histogramming
# import matplotlib.pyplot as plt  # for plotting
# import plotly.graph_objects as go
# from lmfit.models import PolynomialModel, GaussianModel  # for signal and background fits
# import vector  # for handling 4-vectors
# from matplotlib.ticker import MaxNLocator, AutoMinorLocator  # for customizing plot ticks

# def run(selected_tab=None):
#     st.title("Analyses")
#     st.write("This tab focuses on the Higgs boson decay to two Z bosons (H->ZZ).")
#     # ATLAS Open Data directory
#     path = "https://atlas-opendata.web.cern.ch/atlas-opendata/13TeV/GamGam/Data/"
#     samples_list = ['data15_periodD', 'data15_periodE', 'data15_periodF', 'data15_periodG',
#                     'data15_periodH', 'data15_periodJ', 'data16_periodA', 'data16_periodB',
#                     'data16_periodC', 'data16_periodD', 'data16_periodE', 'data16_periodF',
#                     'data16_periodG', 'data16_periodK', 'data16_periodL']

#     variables = ["photon_pt", "photon_eta", "photon_phi", "photon_e", 
#                 "photon_isTightID", "photon_ptcone20"]

#     # Add Streamlit controls
#     st.write("This application allows you to rediscover the Higgs boson using ATLAS Open Data.")

#     # User input for the lower cut on photon transverse momentum (pt)
#     pt_lower_cut = st.slider("Set lower cut for photon transverse momentum (pt) in GeV", 0, 100, 40)

#     # Define cuts on photon transverse momentum using Streamlit input
#     def cut_photon_pt(photon_pt):
#         # Only the events where photon_pt[0] > pt_lower_cut and photon_pt[1] > 30 GeV are kept
#         return (photon_pt[:, 0] < pt_lower_cut) | (photon_pt[:, 1] < 30)

#     # Cut on the photon reconstruction quality
#     def cut_photon_reconstruction(photon_isTightID):
#         return (photon_isTightID[:, 0] == False) | (photon_isTightID[:, 1] == False)

#     # Cut on the energy isolation
#     def cut_isolation_pt(photon_ptcone20):
#         return (photon_ptcone20[:, 0] > 4) | (photon_ptcone20[:, 1] > 4)

#     # Cut on the pseudorapidity in barrel/end-cap transition region
#     def cut_photon_eta_transition(photon_eta):
#         condition_0 = (np.abs(photon_eta[:, 0]) < 1.52) & (np.abs(photon_eta[:, 0]) > 1.37)
#         condition_1 = (np.abs(photon_eta[:, 1]) < 1.52) & (np.abs(photon_eta[:, 1]) > 1.37)
#         return condition_0 | condition_1

#     # Calculate the invariant mass of the 2-photon state
#     def calc_mass(photon_pt, photon_eta, photon_phi, photon_e):
#         p4 = vector.zip({"pt": photon_pt, "eta": photon_eta, "phi": photon_phi, "e": photon_e})
#         invariant_mass = (p4[:, 0] + p4[:, 1]).M  # .M calculates the invariant mass
#         return invariant_mass

#     # Placeholder for data analysis
#     all_data = []
#     sample_data = []

#     # Loop over each sample in samples_list
#     st.write("Processing data samples...")
#     for val in samples_list:
#         fileString = path + val + ".root"

#         with uproot.open(fileString + ":analysis") as t:
#             tree = t

#         for data in tree.iterate(variables, library="ak"):
#             photon_isTightID = data['photon_isTightID']
#             data = data[~cut_photon_reconstruction(photon_isTightID)]
            
#             photon_pt = data['photon_pt']
#             data = data[~cut_photon_pt(photon_pt)]

#             photon_ptcone20 = data['photon_ptcone20']
#             data = data[~cut_isolation_pt(photon_ptcone20)]

#             photon_eta = data['photon_eta']
#             data = data[~cut_photon_eta_transition(photon_eta)]

#             data['mass'] = calc_mass(data['photon_pt'], data['photon_eta'], data['photon_phi'], data['photon_e'])
#             sample_data.append(data)

#     # Concatenate the data into a final dataset
#     if sample_data:
#         all_data = ak.concatenate(sample_data)
#         st.write("Data processed successfully!")
#     else:
#         st.write("No data available after applying cuts.")

#     # x-axis range of the plot
#     xmin = 100 #GeV
#     xmax = 160 #GeV

#     # Histogram bin setup
#     step_size = 3 #GeV
#     bin_edges = np.arange(start=xmin, # The interval includes this value
#                         stop=xmax+step_size, # The interval doesn't include this value
#                         step=step_size ) # Spacing between values
#     bin_centres = np.arange(start=xmin+step_size/2, # The interval includes this value
#                             stop=xmax+step_size/2, # The interval doesn't include this value
#                             step=step_size ) # Spacing between values

#     # Plot the invariant mass histogram with signal + background fit
#     if len(all_data) > 0:
#         st.write("Plotting the invariant mass and performing fits...")
        
#         data_x,_ = np.histogram(ak.to_numpy(all_data['mass']), 
#                                     bins=bin_edges ) # histogram the data
#         data_x_errors = np.sqrt( data_x ) # statistical error on the data

#         # data fit
#         polynomial_mod = PolynomialModel( 4 ) # 4th order polynomial
#         gaussian_mod = GaussianModel() # Gaussian

#         # set initial guesses for the parameters of the polynomial model
#         # c0 + c1*x + c2*x^2 + c3*x^3 + c4*x^4
#         pars = polynomial_mod.guess(data_x, # data to use to guess parameter values
#                                     x=bin_centres, c0=data_x.max(), c1=0,
#                                     c2=0, c3=0, c4=0 )

#         # set initial guesses for the parameters of the Gaussian model
#         pars += gaussian_mod.guess(data_x, # data to use to guess parameter values
#                                 x=bin_centres, amplitude=100, 
#                                 center=125, sigma=2 )

#         model = polynomial_mod + gaussian_mod # combined model

#         # fit the model to the data
#         out = model.fit(data_x, # data to be fit
#                         pars, # guesses for the parameters
#                         x=bin_centres, weights=1/data_x_errors ) #ASK

#         # background part of fit
#         params_dict = out.params.valuesdict() # get the parameters from the fit to data
#         c0 = params_dict['c0'] # c0 of c0 + c1*x + c2*x^2 + c3*x^3 + c4*x^4
#         c1 = params_dict['c1'] # c1 of c0 + c1*x + c2*x^2 + c3*x^3 + c4*x^4
#         c2 = params_dict['c2'] # c2 of c0 + c1*x + c2*x^2 + c3*x^3 + c4*x^4
#         c3 = params_dict['c3'] # c3 of c0 + c1*x + c2*x^2 + c3*x^3 + c4*x^4
#         c4 = params_dict['c4'] # c4 of c0 + c1*x + c2*x^2 + c3*x^3 + c4*x^4

#         # get the background only part of the fit to data
#         background = c0 + c1*bin_centres + c2*bin_centres**2 + c3*bin_centres**3 + c4*bin_centres**4

#         # data fit - background fit = signal fit
#         signal_x = data_x - background 

#         # Main plot (Signal + Background Fit)
#         main_trace_data = go.Scatter(
#             x=bin_centres, y=data_x, mode='markers',
#             error_y=dict(type='data', array=data_x_errors, visible=True),
#             name='Data', marker=dict(color='black')
#         )

#         # Signal + Background Fit (best fit from your lmfit output)
#         main_trace_fit = go.Scatter(
#             x=bin_centres, y=out.best_fit, mode='lines',
#             name='Sig+Bkg Fit ($m_H=125$ GeV)', line=dict(color='red')
#         )

#         # Background-only fit
#         main_trace_background = go.Scatter(
#             x=bin_centres, y=background, mode='lines',
#             name='Bkg (4th order polynomial)', line=dict(dash='dash', color='red')
#         )

#         # Residual plot (Data - Background)
#         residual_trace = go.Scatter(
#             x=bin_centres, y=data_x - background, mode='markers',
#             error_y=dict(type='data', array=data_x_errors, visible=True),
#             name='Data - Background', marker=dict(color='black')
#         )

#         # Create subplots: main plot and residual plot
#         from plotly.subplots import make_subplots

#         fig = make_subplots(
#             rows=2, cols=1, shared_xaxes=True, 
#             vertical_spacing=0.15, subplot_titles=('Main Plot', 'Residual Plot'),
#             row_heights=[0.7, 0.3]
#         )

#         # Add main plot traces
#         fig.add_trace(main_trace_data, row=1, col=1)
#         fig.add_trace(main_trace_fit, row=1, col=1)
#         fig.add_trace(main_trace_background, row=1, col=1)

#         # Add residual plot trace
#         fig.add_trace(residual_trace, row=2, col=1)

#         # Update axis labels and layout
#         fig.update_xaxes(title_text="di-photon invariant mass $m_{\gamma\gamma}$ [GeV]", row=2, col=1)
#         fig.update_yaxes(title_text=f"Events / {int(np.diff(bin_centres).mean())} GeV", row=1, col=1)
#         fig.update_yaxes(title_text="Events - Bkg", row=2, col=1)

#         # Add annotations (optional, based on your original plot)
#         fig.add_annotation(
#             x=0.2, y=0.92, xref="paper", yref="paper", showarrow=False,
#             text="ATLAS Open Data", font=dict(size=13), row=1, col=1
#         )
#         fig.add_annotation(
#             x=0.2, y=0.86, xref="paper", yref="paper", showarrow=False,
#             text="for education", font=dict(size=10), row=1, col=1  # Removed style='italic'
#         )
#         fig.add_annotation(
#             x=0.2, y=0.80, xref="paper", yref="paper", showarrow=False,
#             text=r'$\sqrt{s}$=13 TeV, $\int$L dt = 36.1 fb$^{-1}$', font=dict(size=10), row=1, col=1
#         )
#         fig.add_annotation(
#             x=0.2, y=0.74, xref="paper", yref="paper", showarrow=False,
#             text=r'$H \rightarrow \gamma\gamma$', font=dict(size=12), row=1, col=1
#         )

#         # Update layout to improve spacing and titles
#         fig.update_layout(
#             height=700, width=800,
#             title_text="Invariant Mass of di-photon System with Signal + Background Fit",
#             hovermode="x unified"
#         )

#         # Show the figure in Streamlit
#         st.plotly_chart(fig, use_container_width=True)

#     else:
#         st.write("No events to plot after applying cuts.")

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
    folder = "analyses"

    # Initialize session state for expanded state of sections
    if "expanded_intro" not in st.session_state:
        st.session_state["expanded_intro"] = False
    if "expanded_histograms" not in st.session_state:
        st.session_state["expanded_histograms"] = False

    # Create paths and titles for each section
    tabs_path = ['01_Zpeak.md']
    tab_titles = get_first_level_headers(selected_language, folder, tabs_path)

    st.title("Physics Analyses")
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

    # # Tab 2: Histograms
    # with tabs[1]:
    #     # Load preview for histograms
    #     histograms_preview = load_markdown_preview(tabs_path[1], folder, selected_language, lines=3)

    #     if not st.session_state["expanded_histograms"]:
    #         # Show preview
    #         preview_lines = histograms_preview.splitlines()
    #         st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
    #         st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
    #         if st.button("Read more", key="histograms_read"):
    #             st.session_state["expanded_histograms"] = True
    #             st.rerun()  # Refresh the app to display the full content
    #     else:
    #         # Show full content
    #         load_markdown_file_with_images_and_code(tabs_path[1], folder, global_namespace, selected_language)
    #         if st.button("Done!", key="histograms_done"):
    #             st.session_state["expanded_histograms"] = False
    #             st.rerun()  # Refresh the app to show the preview again
