import streamlit as st
from streamlit_theme import st_theme
import numpy as np
import uproot # for reading .root files
import awkward as ak # for handling complex and nested data structures efficiently
import pandas as pd
from utils_analysis import *
from PIL import Image
import base64
import os
import json
import random
import time

                
def run(selected_language):
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

    # Initialize flags to keep track of each step
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False

    if 'nlepton_cut_applied' not in st.session_state:
        st.session_state.nlepton_cut_applied = False

    if 'leptontype_cut_applied' not in st.session_state:
        st.session_state.leptontype_cut_applied = False

    if 'leptoncharge_cut_applied' not in st.session_state:
        st.session_state.leptoncharge_cut_applied = False

    if 'leptonpt_cut_applied' not in st.session_state:
        st.session_state.leptonpt_cut_applied = False

    if 'invariant_mass_calculated' not in st.session_state:
        st.session_state.invariant_mass_calculated = False
    
    if 'mc_loaded' not in st.session_state:
        st.session_state.mc_loaded = False

    # Initialize a special session state variable for the selectbox
    # This is so that the first cut option resets when using the reset analysis button
    if 'n_leptons_selection' not in st.session_state:
        st.session_state['n_leptons_selection'] = "--"

    # Initilize the expanders for the quizzes
    # First time they are expanded, when reseting they are not
    if 'expand_all' not in st.session_state:
        st.session_state['expand_all'] = True

    # Initialize session state for hint on lepton cut
    if 'show_hint' not in st.session_state:
        st.session_state['show_hint'] = False

    # Define a function to toggle the hint
    def toggle_hint():
        st.session_state['show_hint'] = not st.session_state['show_hint']

    if 'is_higgs' not in st.session_state:
        st.session_state['is_higgs'] = False

    # Get the current theme using st_theme
    theme = st_theme()

    # This is the json with all the info for all analyses
    # Build the path to the JSON file
    json_file_path = os.path.join('analyses', 'event_counts.json')
    # Open and load the JSON file
    with open(json_file_path, 'r') as json_file:
        analyses = json.load(json_file)


    ################ HERE IS WERE THE APP STARTS ################
    st.title("Discover the Z and the Higgs Bosons by Yourself!")

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
        'Select luminosity (fb$^{-1}$):', 
        min_value=12, 
        max_value=36, 
        step=12, 
        value=12
    )

    if st.button("Open the data"):
        # Reset the steps, so that people cannot break it clicking again
        # Reset info for the events
        if st.session_state.nlepton_cut_applied:
            # Reset flags
            st.session_state.nlepton_cut_applied = False
            st.session_state.leptontype_cut_applied = False
            st.session_state.leptoncharge_cut_applied = False
            st.session_state.invariant_mass_calculated = False
            st.session_state.mc_loaded = False
            st.session_state.is_higgs = False

            # Delete the widget keys from session_state
            for key in ['n_leptons_selection', 'flavor_selection', 'charge_pair_selection']:
                if key in st.session_state:
                    del st.session_state[key]
        
        # Reading the data
        random_sleep = random.randint(1, lumi)
        # Display a spinner with the loading message
        with st.spinner("Loading data... Please wait."):
            # Simulate a time-consuming process with a random sleep
            time.sleep(random_sleep)

        st.session_state.data_loaded = True
        st.toast('Data loaded successfully!', icon='📈')
        
    if st.session_state.data_loaded:
        st.info(f" Initial number of events: {analyses[f'{lumi}']['nEvents']}")

        with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
            st.markdown("##### ⁉️ Understanding Luminosity")
            st.markdown(f"""
            You selected a luminosity of **{lumi} fb⁻¹**. But what does luminosity actually represent in a particle physics experiment?
            """)

            possible = ['The amount of time the detector is active',
                        'The number of collisions per second',
                        'A measure of the total number of collisions over a period of time',
                        'The energy at which the collisions happen']
            answer = st.radio("Choose your answer:", possible, index=None)

            if answer == possible[2]:
                st.success("Correct! Luminosity represents the total number of collisions in the dataset. The more luminosity, the better chance of seeing rare events like the Higgs boson.")
            elif answer:
                st.error("Incorrect. Try again or read more about luminosity!")

        # Using a selectbox to let users choose between amounts of leptons
        st.markdown("## Number of leptons in the final state")
        st.markdown("In particle physics, the final state refers to the particles that emerge from a collision, which are detected and analyzed. By identifying the final state, we can infer what happened during the collision. One important aspect is the number of leptons in the final state, as different processes produce different numbers of leptons.")
        st.markdown("Below is a Feynman diagram showing a typical process that results in a final state with two leptons:")
        # Diagram for Z decay
        image_zdecay = f"images/Z_decay_{theme['base']}.png"
        # Encode the image in base64
        with open(image_zdecay, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        # Display the image centered and resizable using HTML with CSS
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{encoded_string}" alt="Centered Image" 
                    style="width: 50%; max-width: 500px; height: auto;">
                <figcaption style="font-size: 0.9em; color: gray;">Z boson decay into two leptons.</figcaption>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("More complex decays may involve more leptons in the final state:")
        # Diagram for H decay
        image_zdecay = f"images/higgs4l_decay_{theme['base']}.png"
        # Encode the image in base64
        with open(image_zdecay, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        # Display the image centered and resizable using HTML with CSS
        st.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{encoded_string}" alt="Centered Image" 
                    style="width: 50%; max-width: 500px; height: auto;">
                <figcaption style="font-size: 0.9em; color: gray;">Higgs boson decay into Z bosons, and subsequently into leptons.</figcaption>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("Below you can see the count of number of leptons in the whole dataset. You can see that, in general, is more common to have fewer leptons in an event.")
        # Get the appropriate plot file based on the theme
        st.image(f"images/lepton_plot_{theme['base']}.png")

        st.markdown("Study the diagrams and the data, and select how many leptons you expect to observe in your final state depending on the analysis you are doing.")

        # Define the options
        n_leptons_options = ("--", 2, 3, 4)

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
        # We define a variable to avoid the page breaking when clicked more than once
        if st.button("Apply number-of-leptons cut"):
            if st.session_state.nlepton_cut_applied:
                st.toast("You already applied a cut. To reset the analysis go to the end of the page.", icon='❌')
            elif n_leptons != '--':
                random_sleep = random.randint(1, lumi/3)
                # Display a spinner with the loading message
                with st.spinner("Making cut... Please wait."):
                    # Simulate a time-consuming process with a random sleep
                    time.sleep(random_sleep)
                st.session_state.nlepton_cut_applied = True
                st.toast("Cut applied successfully.", icon='✂️')
            else:
                st.error("Please select a valid number of leptons.")

    # Step 2: Dynamically generate selection for lepton flavors
    if st.session_state.nlepton_cut_applied:
        st.info(f"Events after the cut: {analyses[f'{lumi}'][f'{n_leptons}leptons']['nEvents']}")

        with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
            st.markdown("##### ⁉️ Lepton Final State")
            st.markdown(f"""
            What can the number of leptons indicate?
            """)

            possible_lepton = ['Two leptons indicate a simple decay of a neutral particle, like a Z boson',
                            'Four leptons indicate a more complex decay chain, possibly involving a Higgs boson',
                            'An odd number of leptons suggests an exotic process',
                            'All of the above']
            answer_lepton = st.radio("Choose your answer:", possible_lepton, index=None, key="lepton_selection_quiz")

            if answer_lepton == possible_lepton[3]:
                st.success("Correct! Each option represents a possibility based on your selection.")
            elif answer_lepton:
                st.error("Incorrect. Try thinking about how leptons are produced in pairs.")

        st.markdown("## Let's ensure conservation")
        st.markdown("In particle interactions, certain properties are always conserved, such as *charge* and lepton *flavor*. Understanding these conservation laws helps narrow down the possibilities for what particles are involved in the final state.")
        st.markdown("In your analysis, you can look at the *flavor* of the leptons (whether they are electrons or muons) and their *charge* (positive or negative). The plot below shows the distribution of lepton flavors, with one bar for positively charged and one for negatively charged leptons. This helps identify whether the final state obeys conservation laws.")

        # Display the pre-generated plot based on the theme
        st.image(f"images/lepton_barplot_{theme['base']}.png")
        
        st.markdown("With this in mind, let's select our next cuts. If unsure, scroll up to the Feynmann diagrams above. You may find helpful information there.")

        flavor_options = ["--", 'Same', 'Different']
        flavor = st.selectbox(f'Should the lepton pairs have the same or different flavor?', flavor_options, key=f"flavor_selection")

        if flavor == 'Same':
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
            if st.session_state.leptontype_cut_applied:
                st.toast("You already applied a cut. To reset the analysis go to the end of the page.", icon='❌')
            elif flavor != '--':    
                # Display a spinner with the loading message
                random_sleep = random.randint(1, lumi/3)
                with st.spinner("Making cut... Please wait."):
                    # Simulate a time-consuming process with a random sleep
                    time.sleep(random_sleep)

                # Display the cut result
                st.session_state.leptontype_cut_applied = True
                st.toast("Cut applied successfully.", icon='✂️')

            else:
                st.error("Please select an option for the flavor of leptons.")

    # Step 3: Dynamically generate selection for lepton charges
    if st.session_state.leptontype_cut_applied:
        st.info(f"Events after the cut: {analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}']['nEvents']}")

        # Offer options for charge pairing: Same charge or Opposite charge
        charge_pair_options = ["--",'Same', 'Opposite']
        charge = st.selectbox('Should the lepton pairs have the same or opposite charge', charge_pair_options)

        # Define the condition for the charge mask based on the selection
        if charge == 'Same':
            st.warning("""Lepton pairs with the same charge are unusual because charge is typically conserved in interactions. 
                    However, some more exotic processes or misidentifications could result in same-charge pairs.
                    """)
        elif charge != '--':
            st.success("""You've chosen opposite-charge leptons. Many interactions conserve charge, 
                    so it's typical to see a lepton and its antiparticle produced together, resulting in opposite charges.
                    """)

            # Apply lepton type cut based on flavor selection
        if st.button("Apply lepton charge cut"):
            if st.session_state.leptoncharge_cut_applied:
                st.toast("You already applied a cut. To reset the analysis go to the end of the page.", icon='❌')
            elif charge != '--':
                # Display a spinner with the loading message
                random_sleep = random.randint(1, lumi/3)
                with st.spinner("Making cut... Please wait."):
                    # Simulate a time-consuming process with a random sleep
                    time.sleep(random_sleep)
                    st.session_state.leptoncharge_cut_applied = True

                    # Provide feedback to the user
                    st.toast("Cut applied successfully.", icon='✂️')
            else:
                st.error("Please select an option for the lepton charge.")

        if st.session_state.leptoncharge_cut_applied:
            st.info(f"Events after the cut: {analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['nEvents']}")

        
            with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
                st.markdown("##### ⁉️ Understanding Charge Selection")
                st.markdown(f"""
                You selected lepton pairs with **{charge} charge**. Why is the charge of lepton pairs important in particle physics?
                """)
                possible_charge = [
                    'Charge conservation is a fundamental principle, and decays usually result in particles with opposite charges',
                    'Leptons with the same charge are more common in particle decays like the Z boson decay',
                    'Charge doesn\'t play a significant role in particle interactions',
                    'Same-charge lepton pairs indicate a high-energy collision'
                ]
                
                answer_charge = st.radio("Choose your answer:", 
                                        possible_charge, 
                                        index=None, key="charge_selection_quiz")

                # Checking for the correct answer and giving feedback
                if answer_charge == possible_charge[0]:
                    st.success("Correct! Charge conservation is fundamental in particle physics, and opposite-charge leptons are typical in decays like the Z boson decay.")
                elif answer_charge:
                    st.error("Incorrect. Consider how charge conservation works in decays. Opposite-charge leptons are expected in many standard decays.")

                # Step 4: Cuts on leptons pT only for Higgs
                if n_leptons==4 and flavor=='Same' and charge=='Opposite':
                    st.session_state['is_higgs'] = True

    if st.session_state.leptoncharge_cut_applied and st.session_state['is_higgs']:
        st.markdown("## Cuts on Leptons p$_T$")
        st.markdown("""In our search for the **Higgs boson**, we rely on applying **cuts** to help reveal its unique characteristics amidst a large amount of data. One of the ways we do this is by focusing on a variable called **transverse momentum** (p$_T$), which represents the momentum of particles perpendicular to the beamline.

Each lepton in our data has a p$_T$ value, which we’ve recorded in descending order as **leading** (highest p$_T$), **sub-leading**, and so forth. By examining these values, we can apply cuts to keep data that better resembles the Higgs boson's characteristics, while reducing data less likely to contain it.

One approach to isolating the Higgs is to apply cuts that remove regions where the **background** (data not related to the Higgs) tends to dominate, leaving more events that match our Higgs-like signature. This means setting a lower limit on the p$_T$ for leptons, as higher p$_T$ values are more likely to capture the events we’re interested in.

The plots below show the p$_T$ distributions for the first, second, and third leptons in both signal (Higgs) and background data. Applying cuts to the lower p$_T$ values could help reduce the background and improve the visibility of potential Higgs events.
""")

        # Display initial image
        if not st.session_state['show_hint']:
            st.image(f"images/lepton_pt_{theme['base']}.png", caption="Click for a hint")
        else:
            st.image(f"images/lepton_pt_{theme['base']}_lines.png", caption="Here's a hint")

        st.markdown("With this in mind, let's consider the best lower bound cuts on p$_T$ that would help in filtering out background events while retaining those that are likely Higgs candidates.")
        with st.expander("🔍 Quiz", expanded=True):
            st.markdown("##### ⁉️ Choosing Appropriate Cuts for Lepton p$_T$")

            st.markdown("""
            Based on what we’ve discussed, which of the following cut values would help us focus on Higgs-like events by reducing the background?
            """)

            cut_options = [
                "20, 15, 10 ",
                "25, 20, 15",
                "10, 5, 2",
                "No cuts are necessary"
            ]

            answer_cut = st.radio("Select the best option for p$_T$ cuts:", cut_options, index=None, key="pt_cut_quiz")
            
            st.button("Want a hint? Click here and check the image above" if not st.session_state['show_hint'] else "Hide Hint", on_click=toggle_hint)
            # Checking for correct answer and providing feedback
            if answer_cut == cut_options[0]:
                st.success("Correct! Setting cuts of 20, 15, and 10 on the lepton p$_T$ values can help us focus on Higgs-like events by filtering out background.")
            elif answer_cut:
                st.error("Not quite. Focus on values that effectively reduce background while keeping the Higgs events.")
            

        st.markdown("Now, let's make the cut")

        if st.button("Cut on leptons p$_T$"):
            if st.session_state.leptonpt_cut_applied:
                st.toast("You already applied a cut. To reset the analysis go to the end of the page.", icon='❌')
            else:
                st.session_state.leptonpt_cut_applied = True
                # Display a spinner with the loading message
                random_sleep = random.randint(1, lumi/3)
                with st.spinner("Making cut... Please wait."):
                    # Simulate a time-consuming process with a random sleep
                    time.sleep(random_sleep)
                    st.session_state.leptoncharge_cut_applied = True

                    # Provide feedback to the user
                    st.toast("Cut applied successfully.", icon='✂️')
    
    if st.session_state.leptonpt_cut_applied:
        st.info(f"Events after the cut: {analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons']['nEvents']}")

    # Steep 5: invariant mass plot
    if (st.session_state.leptoncharge_cut_applied and not st.session_state['is_higgs']) or (st.session_state['is_higgs'] and st.session_state.leptoncharge_cut_applied):
        st.markdown("## Unveiling Particles with Invariant Mass")
        st.markdown("The *invariant mass* is a key tool in particle physics. It allows us to reconstruct the mass of particles that are produced in collisions, even if we don't observe them directly. By analyzing the energy and momentum of the leptons in the final state, we can calculate their combined *invariant mass*.")
        st.markdown('This quantity is particularly useful because it is the same in all reference frames—it "remembers" the mass of the particle that decayed into the leptons.')
        st.markdown("When plotted, the invariant mass distribution often shows peaks where particles like the Z boson or Higgs boson appear. These peaks reveal the characteristic mass of the particle, allowing us to \"see\" it even though it's long gone by the time we're analyzing the data.")
        st.markdown("By calculating and plotting the invariant mass, you will be able to observe these peaks and potentially discover particles for yourself!")

        with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
            st.markdown("##### ⁉️ Invariant Mass")
            st.markdown("""
            The invariant mass is a crucial quantity in particle physics. What can it tell us about a particle?
            """)
            possible_mass = ["The energy of the particle", 
                            "The momentum of the particle", 
                            "The rest mass of the particle that produced the leptons", 
                            "The type of particle that decayed"]
            
            answer_mass = st.radio("Choose your answer:", 
                                    possible_mass, 
                                    index=None, key="invariant_mass_selection_quiz")

            if answer_mass == possible_mass[2]:
                st.success("Correct! The invariant mass tells us the mass of the particle that decayed into the leptons.")
            elif answer_mass:
                st.error("Incorrect. Remember, invariant mass relates to the particle's rest mass.")

        if st.button("Calculate and plot invariant mass"):
            if (n_leptons==4) and (flavor=='Same') and (charge=='Opposite'):
                #st.info(f"Events after the cut: {analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons']['nEvents']}")
                st.image('analyses/'+analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}']['ptLeptons'][f"plot_data_only_{theme['base']}"])
            else:
                st.image('analyses/'+analyses[f'{lumi}'][f'{n_leptons}leptons'][f'flavor{flavor}'][f'charge{charge}'][f"plot_data_only_{theme['base']}"])
    
    # Step 6: Discussion
    if st.session_state.invariant_mass_calculated:
        with st.expander("🔍 Quiz", expanded=st.session_state['expand_all']):
            st.markdown("##### ⁉️ Interpreting the Invariant Mass Plot")
            st.markdown("""
            You generated an invariant mass plot. If a peak appears around 91 GeV, which particle might it correspond to?
            """)

            possible_final = ["Higgs boson", "Z boson", "Photon", "Top quark"]
            answer_final = st.radio("Choose your answer:", 
                                    possible_final, 
                                    index=None, key="invariant_mass_quiz")

            if answer_final == possible_final[1]:
                st.success("Correct! A peak around 91 GeV typically corresponds to the Z boson.")
            elif answer_final:
                st.error("Incorrect. Peaks near 91 GeV usually indicate the presence of a Z boson, since 91 GeV is its mass")
        
        if answer_final:
            st.balloons()
            st.markdown("### Discussion")
            st.markdown("You reached the end of the analysis, once you are happy with the result wait for the discussion.")

    # Reset button to start the analysis again
    st.markdown('---')
    st.write("""If you want to reaply cuts click the `Reset analysis` button. 
             Don't worry, you won't need to load the data again! You will start again on the number-of-leptons cut.""")
    if st.button("Reset analysis"):
            # Reset flags
            st.session_state.nlepton_cut_applied = False
            st.session_state.leptontype_cut_applied = False
            st.session_state.leptoncharge_cut_applied = False
            st.session_state.invariant_mass_calculated = False
            st.session_state.mc_loaded = False
            st.session_state['expand_all'] = False

            # Delete the widget keys from session_state
            for key in ['n_leptons_selection', 'flavor_selection', 'charge_pair_selection']:
                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()
            st.toast("Analysis has been reset.")