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

################################################################################################################################################
# import streamlit as st
# import io
# import sys
# import json
# from utils import load_markdown_file_with_images_and_code, get_first_level_headers, load_markdown_preview

# # For the analyses
# import infofile # local file containing cross-sections, sums of weights, dataset IDs
# import numpy as np # for numerical calculations such as histogramming
# import matplotlib.pyplot as plt # for plotting
# from matplotlib.ticker import AutoMinorLocator # for minor ticks
# import uproot # for reading .root files
# import awkward as ak # to represent nested data in columnar format
# import vector # for 4-momentum calculations
# import time

# # Define backend variables and functions that will be available to the user's code
# selected_language = st.session_state.get("language", "english").lower()

# def run(selected_tab=None):
#     # Shared global namespace across all cells
#     global_namespace = {
#         'st': st,  # Provide Streamlit functionalities to users
#         'np': np,  # For numerical calculations
#         'plt': plt,  # For plotting
#         'AutoMinorLocator': AutoMinorLocator,  # For minor ticks
#         'uproot': uproot,  # For reading .root files
#         'ak': ak,  # For handling nested data in columnar format
#         'vector': vector,  # For 4-momentum calculations
#         'time': time,  # Time module
#         'infofile': infofile,  # Local file containing cross-sections, sums of weights, dataset IDs
#     }

#     # Folder where markdown files are stored
#     folder = "analyses"

#     # Initialize session state for expanded state of sections
#     if "expanded_Zpeak" not in st.session_state:
#         st.session_state["expanded_Zpeak"] = False
#     if "expanded_HtoZZ" not in st.session_state:
#         st.session_state["expanded_HtoZZ"] = False

#     # Create paths and titles for each section
#     tabs_path = ['01_Zpeak.md','02_HtoZZ.md']
#     tab_titles = get_first_level_headers(selected_language, folder, tabs_path)

#     st.title("Physics Analyses")
#     st.markdown("Some info about the thing that they will do here.")
     
#     # Create the tabs
#     tabs = st.tabs(tab_titles)

#     # Tab 1: Introduction
#     with tabs[0]:
#         # Load preview for intro
#         Zpeak_preview = load_markdown_preview(tabs_path[0], folder, selected_language, lines=3)
#         HtoZZ_preview = load_markdown_preview(tabs_path[1], folder, selected_language, lines=3)

#         if not st.session_state["expanded_Zpeak"]:
#             # Show preview
#             preview_lines = Zpeak_preview.splitlines()
#             st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
#             st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
#             if st.button("Read more", key="Zpeak_read"):
#                 st.session_state["expanded_Zpeak"] = True
#                 st.rerun()  # Refresh the app to display the full content
#         else:
#             # Show full content
#             load_markdown_file_with_images_and_code(tabs_path[0], folder, global_namespace, selected_language)
#             if st.button("Done!", key="Zpeak_done"):
#                 st.session_state["expanded_Zpeak"] = False
#                 st.rerun()  # Refresh the app to show the preview again

#     # Tab 2: H to ZZ
#     with tabs[1]:
#         # Load preview for histograms
#         histograms_preview = load_markdown_preview(tabs_path[1], folder, selected_language, lines=3)

#         if not st.session_state["expanded_HtoZZ"]:
#             # Show preview
#             preview_lines = HtoZZ_preview.splitlines()
#             st.markdown(f"#{preview_lines[0]}")  # First line as title with larger font
#             st.write("\n".join(preview_lines[1:]))  # Remaining lines as preview text
#             if st.button("Read more", key="HtoZZ_read"):
#                 st.session_state["expanded_HtoZZ"] = True
#                 st.rerun()  # Refresh the app to display the full content
#         else:
#             # Show full content
#             load_markdown_file_with_images_and_code(tabs_path[1], folder, global_namespace, selected_language)
#             if st.button("Done!", key="HtoZZ_done"):
#                 st.session_state["expanded_HtoZZ"] = False
#                 st.rerun()  # Refresh the app to show the preview again

####################################################################################################################################################

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import uproot
import awkward as ak
import vector
import pandas as pd
import infofile
from matplotlib.ticker import AutoMinorLocator

def run(selected_tab=None):
    st.title("Discover the Higgs Boson Yourself!")

    # Introduction
    st.markdown("""
    This app visualizes the final analysis of both data and Monte Carlo simulations in the Higgs boson search.
    You can adjust lepton transverse momentum cuts using the sliders below.
    """)

    # Define paths and samples
    path = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/"

    samples = {
        'data': {
            'list': ['data_A', 'data_B', 'data_C', 'data_D'],  # 2016 data
        },
        r'Background $Z,t\bar{t}$': {
            'list': ['Zee', 'Zmumu', 'ttbar_lep'],
            'color': "#6b59d3"
        },
        r'Background $ZZ^*$': {
            'list': ['llll'],
            'color': "#ff0000"
        },
        r'Signal ($m_H$ = 125 GeV)': {
            'list': ['ggH125_ZZ4lep', 'VBFH125_ZZ4lep', 'WH125_ZZ4lep', 'ZH125_ZZ4lep'],
            'color': "#00cdff"
        }
    }

    # Function to calculate Monte Carlo weights
    def calc_weight(weight_variables, sample, events):
        info = infofile.infos[sample]
        xsec_weight = (lumi*1000*info["xsec"])/(info["sumw"]*info["red_eff"]) #*1000 to go from fb-1 to pb-1
        total_weight = xsec_weight 
        for variable in weight_variables:
            total_weight = total_weight * events[variable]
        return total_weight

    def cut_lep_type_2(lep_type):
        sum_lep_type = lep_type[:, 0] + lep_type[:, 1] 
        lep_type_cut_bool = (sum_lep_type == 22) | (sum_lep_type == 26)
        return lep_type_cut_bool # True means we should remove this entry (lepton type does not match)
    
    def cut_lep_charge_2(lep_charge):
        # first lepton in each event is [:, 0], 2nd lepton is [:, 1] etc
        sum_lep_charge = lep_charge[:, 0] + lep_charge[:, 1] == 0
        return sum_lep_charge # True means we should remove this entry (sum of lepton charges is not equal to 0)

    # Cut lepton type (electron type is 11,  muon type is 13)
    def cut_lep_type(lep_type):
        sum_lep_type = lep_type[:, 0] + lep_type[:, 1] + lep_type[:, 2] + lep_type[:, 3]
        lep_type_cut_bool = (sum_lep_type == 44) | (sum_lep_type == 48) | (sum_lep_type == 52)
        return lep_type_cut_bool # True means we should remove this entry (lepton type does not match)

    # Cut lepton charge
    def cut_lep_charge(lep_charge):
        # first lepton in each event is [:, 0], 2nd lepton is [:, 1] etc
        sum_lep_charge = lep_charge[:, 0] + lep_charge[:, 1] + lep_charge[:, 2] + lep_charge[:, 3] == 0
        return sum_lep_charge # True means we should remove this entry (sum of lepton charges is not equal to 0)

    # Function to apply cuts based on sliders
    def apply_cuts(data, pt_cut1, pt_cut2):
        # Cuts
        cut_leading_pt = data['lep_pt'][:, 0] > pt_cut1 * 0.001
        cut_subleading_pt = data['lep_pt'][:, 1] > pt_cut2 * 0.001
        return data[cut_leading_pt & cut_subleading_pt]

    def calc_mass_2(pt, eta, phi, E):
        p4 = vector.zip({"pt": pt, "eta": eta, "phi": phi, "E": E})
        return (p4[:, 0] + p4[:, 1]).M * 0.001  # Convert MeV to GeV
    
    # Function to calculate invariant mass
    def calc_mass(pt, eta, phi, E):
        p4 = vector.zip({"pt": pt, "eta": eta, "phi": phi, "E": E})
        return (p4[:, 0] + p4[:, 1] + p4[:, 2] + p4[:, 3]).M * 0.001  # Convert MeV to GeV

    def do_plot(bin_centres, bin_edges, data_x, data_x_errors, mc_x, mc_weights, mc_labels, lep='Four'):
        # Main plot
        fig, main_axes = plt.subplots()

        # Plot the data points with larger bins and better spacing
        main_axes.errorbar(x=bin_centres, y=data_x, yerr=data_x_errors, fmt='ko', label='Data')

        if lep == "Four":
            # Plot the Monte Carlo bars with adjusted bins
            mc_heights = main_axes.hist(mc_x, bins=bin_edges, weights=mc_weights, stacked=True, color=mc_colors, label=mc_labels)
            mc_x_tot = mc_heights[0][-1]

            # Calculate MC statistical uncertainty: sqrt(sum w^2)
            mc_x_err = np.sqrt(np.histogram(np.hstack(mc_x), bins=bin_edges, weights=np.hstack(mc_weights)**2)[0])

            # Plot the signal on top of the backgrounds
            signal_heights = main_axes.hist(signal_x, bins=bin_edges, bottom=mc_x_tot, weights=signal_weights, color=signal_color, label=r'Signal ($m_H$ = 125 GeV)')

            # Plot the statistical uncertainty with a better approach
            main_axes.bar(bin_centres, 2 * mc_x_err, alpha=0.5, bottom=mc_x_tot - mc_x_err, color='none', hatch="////", width=step_size, label='Stat. Unc.')

        # Set plot limits, labels, and legend
        main_axes.set_xlim(left=xmin, right=xmax)
        main_axes.set_xlabel(r'4-lepton invariant mass $\mathrm{m_{4l}}$ [GeV]', fontsize=13)
        main_axes.set_ylabel(f'Events / {step_size} GeV')

        # Add minor ticks
        main_axes.xaxis.set_minor_locator(AutoMinorLocator())
        main_axes.yaxis.set_minor_locator(AutoMinorLocator())

        # Add text annotations
        main_axes.text(0.05, 0.93, 'ATLAS Open Data', transform=main_axes.transAxes, fontsize=13)
        main_axes.text(0.05, 0.88, 'for education', transform=main_axes.transAxes, style='italic', fontsize=8)
        lumi_used = str(lumi * fraction)
        main_axes.text(0.05, 0.82, f'$\sqrt{{s}}$=13 TeV,$\\int$L dt = {lumi_used} fb$^{{-1}}$', transform=main_axes.transAxes)
        if lep== "Four":
            main_axes.text(0.05, 0.76, r'$H \rightarrow ZZ^* \rightarrow 4\ell$', transform=main_axes.transAxes)
        elif lep =='Two':
            main_axes.text(0.05, 0.76, r'$H \rightarrow ZZ^*$', transform=main_axes.transAxes)

        # Draw the legend
        main_axes.legend(frameon=False)

        # Display the plot
        st.pyplot(fig)

    # Set luminosity to 10 fb-1 for all data
    lumi = 10
    fraction = 1.0  # Fraction of events to process
    variables = ['lep_pt', 'lep_eta', 'lep_phi', 'lep_E', 'lep_charge', 'lep_type']
    weight_variables = ["mcWeight", "scaleFactor_PILEUP", "scaleFactor_ELE", "scaleFactor_MUON", "scaleFactor_LepTRIGGER"]

    # Using a selectbox to let users choose between different cut strategies or samples
    many_leptons = st.selectbox(
        'How many leptons do you want to look for?',
        ('Two', 'Four')
    )

    # Sliders for cuts
    st.markdown("### Adjust lepton $p_T$ cuts")
    leading_pt_cut = st.slider('Leading Lepton $p_T$ Cut (GeV)', 0, 100, 0, 10)
    subleading_pt_cut = st.slider('Sub-leading Lepton $p_T$ Cut (GeV)', 0, 100, 0, 10)

    # Assign value based on the option chosen
    if many_leptons == 'Two':
        lepton_type_cut = cut_lep_type_2
        lepton_charge_cut = cut_lep_charge_2
    elif many_leptons == 'Four':
        lepton_type_cut = cut_lep_type
        lepton_charge_cut = cut_lep_charge
    else:
        st.write("Invalid option")


    # Loop through samples and process the data
    all_data = {}
    for s in samples: 
        st.write('Processing ' + s + ' samples')

        # Define empty list to hold data
        frames = [] 
        for val in samples[s]['list']: 
            prefix = "Data/" if s == 'data' else "MC/mc_" + str(infofile.infos[val]["DSID"]) + "."
            fileString = path + prefix + val + ".4lep.root"

            with uproot.open(fileString + ":mini") as t:
                tree = t

            sample_data = []
            for data in tree.iterate(variables + weight_variables, library="ak", entry_stop=tree.num_entries * fraction):
                # Apply cuts and calculate invariant mass
                # Lepton type and charge
                lep_type = data['lep_type']
                data = data[lepton_type_cut(lep_type)]
                lep_charge = data['lep_charge']
                data = data[lepton_charge_cut(lep_charge)]
                # Cuts on pt of jets
                data = apply_cuts(data, leading_pt_cut, subleading_pt_cut)
                if many_leptons == 'Two':
                    data['mass'] = calc_mass_2(data['lep_pt'], data['lep_eta'], data['lep_phi'], data['lep_E'])
                elif many_leptons == 'Four':
                    data['mass'] = calc_mass(data['lep_pt'], data['lep_eta'], data['lep_phi'], data['lep_E'])

                # Store Monte Carlo weights if not data
                if 'data' not in val:
                    data['totalWeight'] = calc_weight(weight_variables, val, data)
                sample_data.append(data)

            frames.append(ak.concatenate(sample_data))
        all_data[s] = ak.concatenate(frames)
        if many_leptons=='Two':
            break

    # Prepare the bins for plotting
    if many_leptons == 'Two':
        xmin, xmax = 50, 150  # GeV
        step_size = 3  # GeV      
    elif many_leptons == 'Four':
        xmin, xmax = 80, 250  # GeV
        step_size = 5  # GeV

    bin_edges = np.arange(start=xmin, stop=xmax + step_size, step=step_size)
    bin_centres = np.arange(start=xmin + step_size / 2, stop=xmax + step_size / 2, step=step_size)

    # Prepare the histogram data
    data_x, _ = np.histogram(ak.to_numpy(all_data['data']['mass']), bins=bin_edges)
    data_x_errors = np.sqrt(data_x)

    if many_leptons == 'Four':
        signal_x = ak.to_numpy(all_data[r'Signal ($m_H$ = 125 GeV)']['mass'])
        signal_weights = ak.to_numpy(all_data[r'Signal ($m_H$ = 125 GeV)'].totalWeight)
        signal_color = samples[r'Signal ($m_H$ = 125 GeV)']['color']

        mc_x = []
        mc_weights = []
        mc_colors = []
        mc_labels = []

        # Loop over background samples and append their values
        for s in samples:
            if s not in ['data', r'Signal ($m_H$ = 125 GeV)']:
                mc_x.append(ak.to_numpy(all_data[s]['mass']))
                mc_weights.append(ak.to_numpy(all_data[s].totalWeight))
                mc_colors.append(samples[s]['color'])
                mc_labels.append(s)

    st.markdown("### Invariant Mass of 4 Leptons")
    if many_leptons == 'Two':    
        do_plot(bin_centres, bin_edges, data_x, data_x_errors, mc_x=None, mc_weights=None, mc_labels=None,lep=many_leptons)
    elif many_leptons == 'Four':
        do_plot(bin_centres, bin_edges, data_x, data_x_errors, mc_x, mc_weights, mc_labels)