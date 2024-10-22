import streamlit as st
from streamlit_theme import st_theme
import numpy as np
import uproot # for reading .root files
import awkward as ak # for handling complex and nested data structures efficiently
import pandas as pd
from utils_analysis import *

def run(selected_tab=None):
    # Initialize everything needed
    # Define paths and samples
    path = "https://atlas-opendata.web.cern.ch/13TeV/2J2LMET30/"
    sample_data = ['data15_periodD.root',
                'data15_periodE.root',
                'data15_periodF.root',
                'data15_periodG.root',
                'data15_periodH.root',
                'data15_periodJ.root',
                'data16_PeriodI.root',
                'data16_periodA.root',
                'data16_periodB.root',
                'data16_periodC.root',
                'data16_periodD.root',
                'data16_periodE.root',
                'data16_periodF.root',
                'data16_periodG.root',
                'data16_periodK.root',
                'data16_periodL.root' ] 
       
    # Initialize ALL_DATA in session_state
    if 'ALL_DATA' not in st.session_state:
        st.session_state.ALL_DATA = {}
        st.session_state.ALL_DATA['original_data'] = None
        st.session_state.ALL_DATA['data'] = None
        st.session_state.ALL_DATA['MC_data'] = None

    # Initialize variables for keeping track of the cutted events.
    if 'cut_log' not in st.session_state:
        st.session_state.cut_log = []

    # Initialize flags for each step
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False

    if 'nlepton_cut_applied' not in st.session_state:
        st.session_state.nlepton_cut_applied = False

    if 'leptontype_cut_applied' not in st.session_state:
        st.session_state.leptontype_cut_applied = False

    if 'leptoncharge_cut_applied' not in st.session_state:
        st.session_state.leptoncharge_cut_applied = False

    if 'invariant_mass_calculated' not in st.session_state:
        st.session_state.invariant_mass_calculated = False
    
    if 'mc_loaded' not in st.session_state:
        st.session_state.mc_loaded = False

    # Initialize a special session state variable for the selectbox
    # This is for prettyness when using the reset analysis buttons
    if 'n_leptons_selection' not in st.session_state:
        st.session_state['n_leptons_selection'] = "--"

    # Get the current theme using st_theme
    theme = st_theme()

    # These are the variables that we will be using for the data
    variables = ['lep_pt', 'lep_eta', 'lep_phi', 'lep_e', 'lep_charge', 'lep_type']

    ################ HERE IS WERE THE APP STARTS ################
    st.title("Discover the Z and the Higgs Bosons Yourself!")

    # Introduction
    st.markdown("""
    With this interactive app you can discover the Z and the Higgs bosons. 
    By understanding and applying appropiate cuts to the data you will discover the particles yourself!
    """)

    st.markdown("## How much data do you want to use?")
    st.markdown("""Begin your analysis by choosing how much data you'd like to work with. Use the slider below to select the **integrated luminosity**, which is a measure of how much data the ATLAS detector has collected.

The more data you analyze, the better chance you have of spotting rare events like the Higgs boson! But keep in mind, *more data can also mean more processing time*.""")
    
    # Create a slider for luminosity
    lumi = st.slider(
        'Select luminosity (fb-1):', 
        min_value=6, 
        max_value=36, 
        step=6, 
        value=6
    )

    # Display the selected luminosity and corresponding data periods
    st.write(f"Selected Luminosity: {lumi} fb-1")
    fraction = lumi / 36

    if st.button("Open the data"):
        open_data(path, sample_data, variables, lumi)

    if st.session_state.data_loaded:
        st.write("Data loaded successfully.")
        st.write(f"Initial number of events: {st.session_state.total_event_count}")

        # Using a selectbox to let users choose between amounts of leptons
        st.markdown("## Choose the number of leptons in the final state")
        st.markdown("In particle physics, the final state refers to the particles that emerge from a collision, which are detected and analyzed. By identifying the final state, we can infer what happened during the collision. One important aspect is the number of leptons in the final state, as different processes produce different numbers of leptons.")

        st.markdown("Below is a Feynman diagram showing a typical process that results in a final state with two leptons:")
        # Diagram for Z decay
        st.markdown("Some processes may result in more leptons in the final state:")
        # Diagram for H decay
        
        st.markdown("Below you can see the count of number of leptons in the whole dataset. You can see that, in general, is more common to have fewer leptons in an event.")
        # Get the appropriate plot file based on the theme
        plot_nleptons = get_darklight_plot('plot',theme)
        # Display the pre-generated plot based on the theme
        with open(plot_nleptons, "r") as f:
            html_string_nleptons = f.read()
       
        # Use streamlit's HTML component to display the interactive Plotly plot
        st.components.v1.html(html_string_nleptons, height=450, width=800)

        st.markdown("Study the diagrams and the data, and select how many leptons you expect to observe in your final state depending on the analysis you are doing.")

        # Define the options
        n_leptons_options = ("--", 2, 3, 4, 5)

        # Create the selectbox
        n_leptons = st.selectbox(
            'How many leptons do you expect in the final state?',
            n_leptons_options,
            index=0,  # Default index for "--"
            key='n_leptons_selection'
        )

        # Access the selected value from session_state
        n_leptons = st.session_state['n_leptons_selection']

        if n_leptons == 2:
            st.success("""You’ve chosen a final state with **2 leptons**.
                    This suggests you're interested in a process where a single intermediate particle decays into a pair of leptons. 
                    Lepton pairs are common in many particle interactions, especially when considering neutral intermediates""")
        elif n_leptons == 4:
            st.success("""You’re looking at **4 leptons** in the final state. 
                    This often indicates a chain of decays, where multiple intermediate particles decay into pairs of leptons. 
                    Such scenarios are interesting for studying complex interactions""")
        elif n_leptons != '--':
            st.warning("""Having an odd number of leptons is unusual in simple decay processes, as leptons are usually produced in pairs due to conservation laws. 
                    However, this might suggest you're exploring more exotic decay modes. Are you looking for dark matter?
                    """)

        # Number of leptons button
        if st.button("Apply number-of-leptons cut"):
            if n_leptons != '--':
                apply_nleptons_cut(int(n_leptons))  # Pass the number of leptons to the function
            else:
                st.error("Please select a valid number of leptons.")

    # Step 2: Dynamically generate selection for lepton flavors
    if st.session_state.nlepton_cut_applied:
        st.write("Cut applied successfully.")
        st.write(st.session_state.cut_log[-1])

        st.markdown("## Let's ensure conservation")
        st.markdown("n particle interactions, certain properties are always conserved, such as *charge* and lepton *flavor*. Understanding these conservation laws helps narrow down the possibilities for what particles are involved in the final state.")
        st.markdown("In your analysis, you can look at the *flavor* of the leptons (whether they are electrons or muons) and their *charge* (positive or negative). The plot below shows the distribution of lepton flavors, with one bar for positively charged and one for negatively charged leptons. This helps identify whether the final state obeys conservation laws.")
        # Get the appropriate plot file based on the theme
        plot_chargeflavor = get_darklight_plot('barplot',theme)

        # Display the pre-generated plot based on the theme
        with open(plot_chargeflavor, "r") as f:
            html_string_chargeflavor = f.read()

        # Use streamlit's HTML component to display the interactive Plotly plot
        st.components.v1.html(html_string_chargeflavor, height=450, width=800) 
        
        st.markdown("With this in mind, let's select our next cuts:")
        st.info("If unsure, scroll up to the Feynmann diagrams above. You may find helpful information there.")

        flavor_options = ["--", 'Yes', 'No']
        flavor = st.selectbox(f'Should the lepton pairs have the same flavor?', flavor_options, key=f"flavor_selection")

        if flavor == 'Yes':
            st.success("""
                    Selecting leptons of the same flavor means you're considering a scenario where the properties of the leptons are identical, 
                    such as two electrons or two muons. Same-flavor pairs often arise in decays where the particle interaction respects flavor conservation.
                    """)
            
        elif flavor!= '--':
            st.warning("""
                    Choosing leptons of different flavors indicates you're examining a situation where the leptons are not identical, such as one electron and one muon. 
                    While this might occur in some processes, it’s less common in simple decays due to flavor conservation laws.
                    """)
            
        # Apply lepton type cut based on flavor selection
        if st.button("Apply lepton type cut"):
            if flavor != '--':
                apply_lepton_type_cut(n_leptons, flavor)  # Call the function and pass the selected flavor
            else:
                st.error("Please select an option for the flavor of leptons.")

    # Step 3: Dynamically generate selection for lepton charges
    if st.session_state.leptontype_cut_applied:
        st.write("Cut applied and data processed.")
        st.write(st.session_state.cut_log[-1])

        # Offer options for charge pairing: Same charge or Opposite charge
        charge_pair_options = ["--",'Same', 'Opposite']
        charge_pair = st.selectbox('Should the lepton pairs have the same or opposite charge', charge_pair_options)

        # Define the condition for the charge mask based on the selection
        if charge_pair == 'Same':
            st.warning("""Lepton pairs with the same charge are unusual because charge is typically conserved in interactions. 
                    However, some more exotic processes or misidentifications could result in same-charge pairs.
                    """)
        elif charge_pair != '--':
            st.success("""You've chosen opposite-charge leptons. Many interactions conserve charge, 
                    so it's typical to see a lepton and its antiparticle produced together, resulting in opposite charges.
                    """)

            # Apply lepton type cut based on flavor selection
        if st.button("Apply lepton charge cut"):
            if charge_pair != '--':
                apply_lepton_charge_cut(n_leptons, charge_pair)  # Call the function with selected charge pairing
            else:
                st.error("Please select an option for the lepton charge.")

        if st.session_state.leptoncharge_cut_applied:
            st.write("Cut applied and data processed.")
            st.write(st.session_state.cut_log[-1])

    # Step 4: Weights and cuts for the Higgs only
    if st.session_state.leptontype_cut_applied and n_leptons==4 and flavor=='Yes' and charge_pair=='Opposite':
        if st.button("Load MC data"):
            st.session_state.ALL_DATA['MC_data'] = load_mc_data()
            st.session_state.mc_loaded = True
        
        if st.session_state.mc_loaded:
            st.write("Monte Carlo data loaded successfully")

    # Steep 5: invariant mass calculation and plot
    if st.session_state.leptoncharge_cut_applied:
        st.markdown("## Unveiling Particles with Invariant Mass")
        st.markdown("The *invariant mass* is a key tool in particle physics. It allows us to reconstruct the mass of particles that are produced in collisions, even if we don't observe them directly. By analyzing the energy and momentum of the leptons in the final state, we can calculate their combined *invariant mass*.")
        st.markdown('This quantity is particularly useful because it is the same in all reference frames—it "remembers" the mass of the particle that decayed into the leptons.')
        st.markdown("When plotted, the invariant mass distribution often shows peaks where particles like the Z boson or Higgs boson appear. These peaks reveal the characteristic mass of the particle, allowing us to \"see\" it even though it's long gone by the time we're analyzing the data.")
        st.markdown("By calculating and plotting the invariant mass, you will be able to observe these peaks and potentially discover particles for yourself!")

        if st.button("Calculate and plot invariant mass"):
            calculate_invariant_mass(n_leptons)
            # if (n_leptons==4)&(flavor=='Yes')&(charge_pair=='Opposite'):
            #     process_and_plot_higgs_data(st.session_state.ALL_DATA['MC_data'],lumi)
            # else:
            process_and_plot_data(lumi)
    
    # Step 6: Discussion
    if st.session_state.invariant_mass_calculated:
        st.markdown("### Discussion")
        st.markdown("You reached the end of the analysis, once you are happy with the result wait for the discussion.")

    # Reset button to start the analysis again
    st.markdown('---')
    st.write("""If you want to reaply cuts click the `Reset analysis` button. 
             Don't worry, you won't need to load the data again!""")
    if st.button("Reset analysis"):
        if st.session_state.data_loaded and st.session_state.ALL_DATA['original_data'] is not None:
            # Reset 'data' to the original data
            st.session_state.ALL_DATA['data'] = st.session_state.ALL_DATA['original_data']

            # Reset cut logs
            st.session_state.cut_log = []

            # Reset flags
            st.session_state.nlepton_cut_applied = False
            st.session_state.leptontype_cut_applied = False
            st.session_state.leptoncharge_cut_applied = False
            st.session_state.invariant_mass_calculated = False
            st.session_state.mc_loaded = False

            # Delete the widget keys from session_state
            for key in ['n_leptons_selection', 'flavor_selection', 'charge_pair_selection']:
                if key in st.session_state:
                    del st.session_state[key]

            st.write("Analysis has been reset.")
            st.rerun()
        else:
            st.write("No data loaded to reset.")