import streamlit as st
import uproot
import awkward as ak
import vector
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

def get_darklight_plot(plot,theme):
    if theme and theme.get("base") == "dark":
        return f"images/interactive/lepton_{plot}_dark.html"
    else:
        return f"images/interactive/lepton_{plot}_light.html"

def load_mc_data():
    # Load MC mass and weights from pickle files
    mc_samples = {
        'Background $Z,t\\bar{t},t\\bar{t}+V,VVV$': {
            'mass': None,
            'weights': None,
            'color': '#6b59d3'
        },
        'Background $ZZ^*$': {
            'mass': None,
            'weights': None,
            'color': '#ff0000'
        },
        'Signal ($m_H$ = 125 GeV)': {
            'mass': None,
            'weights': None,
            'color': '#00cdff'
        }
    }

    # Match the sample keys with the respective pickle files
    sample_files = {
        'Background $Z,t\\bar{t},t\\bar{t}+V,VVV$': 'processed_mass_Background_Z_ttbar_VVVV.pickle',
        'Background $ZZ^*$': 'processed_mass_Background_ZZ.pickle',
        'Signal ($m_H$ = 125 GeV)': 'processed_mass_Signal.pickle'
    }

    for sample, file_prefix in sample_files.items():
        mass_filename = f'MC/mass/{file_prefix}'
        weight_filename = f'MC/weights/36fb/{file_prefix.replace("mass", "weights")}'  # Assuming weights files have a similar naming pattern

        with open(mass_filename, 'rb') as f_mass, open(weight_filename, 'rb') as f_weights:
            mc_samples[sample]['mass'] = pickle.load(f_mass)
            mc_samples[sample]['weights'] = pickle.load(f_weights)

    return mc_samples

### Functions data processing ###

def lepton_type_cut(lep_type, n_leptons, cut):
    """
    Apply a cut based on the lepton type.
    
    Parameters:
    lep_type (array): The array of lepton types.
    n_leptons (int): The number of leptons expected in the event.
    cut (str): Selected flavor cut ('Yes' for same flavor, 'No' for different flavor).
    
    Returns:
    mask (array): A mask to apply to the data for filtering the events.
    """
    # Check only the first two leptons
    if cut == 'Yes':
        if n_leptons == 2 or n_leptons == 3:
            # For 2 or 3 leptons, we apply the same-flavor cut to the first two leptons
            sum_lep_type = lep_type[:, 0] + lep_type[:, 1]
            mask = (sum_lep_type == 22) | (sum_lep_type == 26)  # Same-flavor: e+e- or mu+mu-
            
            # Ensure that if there is a third lepton, it is an electron or muon
            if n_leptons == 3:
                third_lepton_mask = (lep_type[:, 2] == 11) | (lep_type[:, 2] == 13)  # Allow electron or muon for the third lepton
                mask = mask & third_lepton_mask  # Combine both conditions

        elif n_leptons == 4 or n_leptons == 5:
            # For 4 or 5 leptons, check combinations of four leptons
            sum_lep_type = lep_type[:, 0] + lep_type[:, 1] + lep_type[:, 2] + lep_type[:, 3]
            mask = (sum_lep_type == 44) | (sum_lep_type == 48) | (sum_lep_type == 52)

    elif cut == 'No':
        if n_leptons == 2 or n_leptons == 3:
            # For 2 or 3 leptons, allow different flavor for the first two leptons
            sum_lep_type = lep_type[:, 0] + lep_type[:, 1]
            mask = (sum_lep_type == 24)  # e+mu- or e-mu+
            
            # Ensure that if there is a third lepton, it is an electron or muon
            if n_leptons == 3:
                third_lepton_mask = (lep_type[:, 2] == 11) | (lep_type[:, 2] == 13)  # Allow electron or muon for the third lepton
                mask = mask & third_lepton_mask  # Combine both conditions

        elif n_leptons == 4 or n_leptons == 5:
            # For 4 or 5 leptons, check combinations of four leptons
            sum_lep_type = lep_type[:, 0] + lep_type[:, 1] + lep_type[:, 2] + lep_type[:, 3]
            mask = (sum_lep_type == 48) 

    return mask

def lepton_charge_cut(lep_charge, n_leptons, cut):
    if cut=='Opposite':
        if n_leptons == 2 or n_leptons == 3:
            # For 2 or 3 leptons, the mask is based on the sum of the first two leptons
            sum_lep_charge = lep_charge[:, 0] + lep_charge[:, 1]
            mask = sum_lep_charge == 0
            
        elif n_leptons == 4 or n_leptons == 5:
            # For 4 or 5 leptons, the mask checks combinations of four leptons
            sum_lep_charge_first = lep_charge[:, 0] + lep_charge[:, 1]
            sum_lep_charge_second = lep_charge[:, 2] + lep_charge[:, 3]
            mask = (sum_lep_charge_first == 0) & (sum_lep_charge_second == 0)

    elif cut=='Same':
        if n_leptons == 2 or n_leptons == 3:
            # For 2 or 3 leptons, the mask is based on the sum of the first two leptons
            sum_lep_charge = lep_charge[:, 0] + lep_charge[:, 1]
            mask = (sum_lep_charge == 2)|(sum_lep_charge == -2)
            
        elif n_leptons == 4 or n_leptons == 5:
            # For 4 or 5 leptons, the mask checks combinations of four leptons
            sum_lep_charge_first = lep_charge[:, 0] + lep_charge[:, 1]
            sum_lep_charge_second = lep_charge[:, 2] + lep_charge[:, 3]
            mask = ((sum_lep_charge_first == 2)|(sum_lep_charge_first == -2))&((sum_lep_charge_second == 2)|(sum_lep_charge_second == -2))
    
    return mask

def invariant_mass(pt, eta, phi, E, n_leptons):
    p4 = vector.zip({"pt": pt, "eta": eta, "phi": phi, "E": E})
    try:
        if n_leptons == 2:
            mass = (p4[:, 0] + p4[:, 1]).M
        elif n_leptons == 3:
            mass = (p4[:, 0] + p4[:, 1] + p4[:, 2]).M
        elif n_leptons == 4:
            mass = (p4[:, 0] + p4[:, 1] + p4[:, 2] + p4[:, 3]).M
        elif n_leptons == 5:
            mass = (p4[:, 0] + p4[:, 1] + p4[:, 2] + p4[:, 3]+ + p4[:, 4]).M

    except IndexError as e:
        # If there is an index error, print the event causing the issue
        st.write(f"IndexError: {str(e)}")
        st.write("Event causing the error:")
        st.write("pt:", pt)
        st.write("eta:", eta)
        st.write("phi:", phi)
        st.write("E:", E)
        st.write(f"Number of leptons expected: {n_leptons}")
        st.write(f"Lepton count in this event: {ak.num(pt)}")
        raise  # Re-raise the exception so it still halts execution

    return mass

### Functions for buttons ###

def open_data(path, sample_data, variables, lumi):
    """
    Function to open ROOT files and load the data into session_state.
    
    Parameters:
    path (str): Path to the data files.
    sample_data (list): List of ROOT data files.
    variables (list): List of variables to be loaded from ROOT files.
    lumi (float): The selected luminosity (fb-1).
    
    Returns:
    None
    """
    frames = []  # List to hold loaded data for each sample
    total_event_count = 0  # Variable to count the total number of events
    fraction = lumi / 36  # Scale the luminosity as a fraction

    # Loop over each ROOT file
    for val in sample_data:
        fileString = path + "Data/" + val  # Path for data files

        # Open the ROOT file
        with uproot.open(fileString) as file:
            # Access the 'analysis' tree
            tree = file["analysis"]

            # Determine the number of entries to read
            entry_stop = int(tree.num_entries * fraction)

            # Read the data from the tree
            data = tree.arrays(variables, library="ak", entry_stop=entry_stop)
            
            # Append data to frames
            frames.append(data)

            # Update total event count
            total_event_count += len(data)

    # Concatenate all frames to get the full data
    if frames:
        full_data = ak.concatenate(frames)
    else:
        full_data = ak.Array([])  # Empty array if no data

    # Store the original data
    st.session_state.ALL_DATA['original_data'] = full_data
    # Store the loaded data in session_state
    st.session_state.ALL_DATA['data'] = full_data

    # Mark that data has been successfully loaded
    st.session_state.data_loaded = True
    st.session_state.total_event_count = len(full_data)

def apply_nleptons_cut(n_leptons):
    """
    Apply a cut based on the selected number of leptons and ensure that all events have exactly n_leptons.
    
    Parameters:
    n_leptons (int): The number of leptons expected in the final state.
    
    Returns:
    None
    """

    if 'data' in st.session_state.ALL_DATA:
        st.session_state.initial_event_count = len(st.session_state.ALL_DATA['data'])  # Total number of events before cut
        st.session_state.filtered_event_count = 0

        # Get the data
        data = st.session_state.ALL_DATA['data']

        # Apply n_leptons cut
        num_particles = ak.num(data['lep_type'])  # Number of leptons in each event
        mask = num_particles == n_leptons  # Create a mask for the correct number of leptons

        # Filter the data based on the number of leptons
        filtered_data = data[mask]

        # Check if any event has a different number of leptons
        num_particles_after_cut = ak.num(filtered_data['lep_type'])  # Number of leptons after the cut
        if not ak.all(num_particles_after_cut == n_leptons):
            st.error(f"Error: Some events do not have exactly {n_leptons} leptons after the cut.")

        # Count the number of events after the cut
        st.session_state.filtered_event_count = len(filtered_data)

        # Update the data in session_state with the filtered data
        st.session_state.ALL_DATA['data'] = filtered_data

        # Log the results of the current cut
        cut_result = f"Number of leptons = {n_leptons}: Events before = {st.session_state.initial_event_count}, Events after = {st.session_state.filtered_event_count}"
        st.session_state.cut_log.append(cut_result)

        # Set flag to indicate the cut has been applied
        st.session_state.nlepton_cut_applied = True
    else:
        st.error("No data available. Please load the data first.")

def apply_lepton_type_cut(n_leptons, flavor):
    """
    Apply a cut based on the selected lepton flavor type and print debugging information.
    
    Parameters:
    n_leptons (int): The number of leptons in the final state.
    flavor (str): Selected flavor cut ('Yes' for same flavor, 'No' for different flavor).
    
    Returns:
    None
    """
    
    if 'data' in st.session_state.ALL_DATA:
        st.write("Applying lepton type cut on existing data...")

        # Retrieve the already filtered data
        data = st.session_state.ALL_DATA['data']

        # Get the lepton type data
        lep_type = data['lep_type']

        # Apply the lepton type cut using the custom function `lepton_type_cut`
        try:
            filtered_data = data[lepton_type_cut(lep_type, n_leptons, flavor)]  # Filter the data
        except Exception as e:
            st.error(f"Error applying lepton type cut: {e}")
            
            # Print the problematic event for debugging
            st.write(f"Lepton type values before the error: {lep_type}")
            st.write(f"Number of leptons expected: {n_leptons}")
            st.write(f"Flavor selection: {flavor}")
            
            # Return early to avoid further errors
            return

        # Check if the filtered data still has the correct number of leptons
        num_leptons_after_cut = ak.num(filtered_data['lep_type'])
        if not ak.all(num_leptons_after_cut >= n_leptons):
            st.warning(f"Some events have fewer than {n_leptons} leptons after the lepton type cut.")
            st.write(f"Number of leptons in events after the cut: {num_leptons_after_cut}")
        
        # Update st.session_state.ALL_DATA with the newly filtered data
        st.session_state.ALL_DATA['data'] = filtered_data

        # Log the results of the current cut and display immediately
        cut_result = f"Lepton type cut (flavor: {flavor}): Events before = {len(data)}, Events after = {len(filtered_data)}"
        st.session_state.cut_log.append(cut_result)

        # Set flag to indicate the cut has been applied
        st.session_state.leptontype_cut_applied = True

    else:
        st.error("No data available. Please run the initial cut first.")

def apply_lepton_charge_cut(n_leptons, charge_pair):
    """
    Apply a cut based on the selected lepton charge pairing.
    
    Parameters:
    n_leptons (int): The number of leptons in the final state.
    charge_pair (str): Selected charge pairing ('Same' or 'Opposite').
    
    Returns:
    None
    """

    if 'data' in st.session_state.ALL_DATA:
        st.write("Applying lepton charge cut on existing data...")

        # Retrieve the already filtered data
        data = st.session_state.ALL_DATA['data']

        # Get the lepton charge data
        lep_charge = data['lep_charge']

        # Apply the lepton charge cut using the custom function `lepton_charge_cut`
        filtered_data = data[lepton_charge_cut(lep_charge, n_leptons, charge_pair)]  # Filter the data

        # Update st.session_state.ALL_DATA with the newly filtered data
        st.session_state.ALL_DATA['data'] = filtered_data

        # Log the results of the current cut and display immediately
        cut_result = f"Lepton charge cut (charge: {charge_pair}): Events before = {len(data)}, Events after = {len(filtered_data)}"
        st.session_state.cut_log.append(cut_result)

        # Set flag to indicate the cut has been applied
        st.session_state.leptoncharge_cut_applied = True

    else:
        st.error("No data available. Please run the initial cut first.")

def calculate_invariant_mass(n_leptons):
    """
    Function to calculate the invariant mass for the given number of leptons.
    Updates the st.session_state with the new mass data.
    
    Parameters:
    n_leptons (int): Number of leptons in the final state (2 or 4).
    
    Returns:
    None
    """
    if 'data' in st.session_state.ALL_DATA:
        # Retrieve the already filtered data
        data = st.session_state.ALL_DATA['data']

        # Debugging: print the available fields in the data object
        # st.write(f"Available fields: {data.fields}")
        
        # Ensure the necessary fields are present
        if all(field in data.fields for field in ['lep_pt', 'lep_eta', 'lep_phi', 'lep_e']):
            # Calculate the invariant mass
            data['mass'] = invariant_mass(data['lep_pt'], data['lep_eta'], data['lep_phi'], data['lep_e'], n_leptons)
            
            # Update st.session_state with the newly calculated mass
            st.session_state.ALL_DATA['data'] = data

            # Set a flag to indicate that the mass has been calculated
            st.session_state.invariant_mass_calculated = True
        else:
            st.error("Lepton fields are missing in the data. Unable to calculate invariant mass.")
    else:
        st.error("No data available. Please load the data first.")

### Functions for plotting ###
def plot_only_data(bin_centres, bin_edges, data_x, data_x_errors, xmin, xmax, step_size, lumi):
        # Create a new figure for the plot
        fig, ax = plt.subplots()

        # Plot the data points with error bars
        ax.errorbar(x=bin_centres, y=data_x, yerr=data_x_errors, fmt='ko', label='Data')

        # Set plot limits, labels, and legend
        ax.set_xlim(left=xmin, right=xmax)
        ax.set_xlabel(r'Invariant mass $\mathrm{m}$ [GeV]', fontsize=13)
        ax.set_ylabel(f'Events / {step_size} GeV', fontsize=13)

        # Add minor ticks to the plot
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

        # Add text annotations
        ax.text(0.05, 0.93, 'ATLAS Open Data', transform=ax.transAxes, fontsize=13)
        ax.text(0.05, 0.88, 'for education', transform=ax.transAxes, style='italic', fontsize=8)
        
        lumi_used = str(lumi)
        ax.text(0.05, 0.82, f'$\sqrt{{s}}$=13 TeV,$\\int$L dt = {lumi_used} fb$^{{-1}}$', transform=ax.transAxes)
        #ax.text(0.05, 0.76, r'$H \rightarrow ZZ^* \rightarrow 2\ell$', transform=ax.transAxes)

        # Add legend
        ax.legend(frameon=False)

        # Display the plot in Streamlit
        st.pyplot(fig)

def process_and_plot_data(lumi):
    """
    Process the filtered data to calculate the two-lepton invariant mass and plot the results.
    
    Parameters:
    n_leptons (int): The number of leptons in the final state.
    lumi (float): The selected luminosity in fb^-1.
    fraction (float): Fraction of data used for plotting.
    
    Returns:
    None
    """
    # Check if there is already processed data from the previous cut
    if st.session_state.invariant_mass_calculated:
        # Retrieve the already filtered data
        data = st.session_state.ALL_DATA['data']

        # Set binning and data variables
        xmin, xmax = 50, 150  # GeV
        step_size = 3  # GeV
        bin_edges = np.arange(start=xmin, stop=xmax + step_size, step=step_size)
        bin_centres = np.arange(start=xmin + step_size / 2, stop=xmax + step_size / 2, step=step_size)

        # Convert data['mass'] to NumPy for binning and plotting
        data_x, _ = np.histogram(ak.to_numpy(data['mass']), bins=bin_edges)
        data_x_errors = np.sqrt(data_x)  # Example errors assuming Poisson statistics

        # Call the function to plot the data
        plot_only_data(bin_centres, bin_edges, data_x, data_x_errors, xmin, xmax, step_size, lumi=lumi)

    else:
        st.write("No data available. Please run the initial cut first.")

def plot_higgs(bin_centres, bin_edges, data_x, data_x_errors, mc_samples, xmin, xmax, step_size, lumi):
    fig, main_axes = plt.subplots()

    # Plot the data points with error bars
    main_axes.errorbar(x=bin_centres, y=data_x, yerr=data_x_errors, fmt='ko', label='Data')

    mc_x = []
    mc_weights = []
    mc_colors = []
    mc_labels = []

    # Extract the MC histograms, weights, and colors
    for sample, sample_info in mc_samples.items():
        mc_x.append(sample_info['mass'])
        mc_weights.append(sample_info['weights'])
        mc_colors.append(sample_info['color'])
        mc_labels.append(sample)

    # Plot the Monte Carlo stacked histograms
    mc_heights = main_axes.hist(mc_x, bins=bin_edges, weights=mc_weights, stacked=True, color=mc_colors, label=mc_labels)
    mc_x_tot = mc_heights[0][-1]  # Total MC values for uncertainty

    # Plot the statistical uncertainty (sqrt of sum of weights squared)
    mc_x_err = np.sqrt(np.histogram(np.hstack(mc_x), bins=bin_edges, weights=np.hstack(mc_weights)**2)[0])
    main_axes.bar(bin_centres, 2 * mc_x_err, alpha=0.5, bottom=mc_x_tot - mc_x_err, color='none', hatch="////", width=step_size, label='Stat. Unc.')

    # Set plot limits, labels, and legend
    main_axes.set_xlim(left=xmin, right=xmax)
    main_axes.set_xlabel(r'4-lepton invariant mass $\mathrm{m_{4l}}$ [GeV]', fontsize=13)
    main_axes.set_ylabel(f'Events / {step_size} GeV')

    # Add minor ticks
    main_axes.xaxis.set_minor_locator(AutoMinorLocator())
    main_axes.yaxis.set_minor_locator(AutoMinorLocator())

    # Add text annotations
    lumi_used = str(lumi)
    main_axes.text(0.05, 0.93, 'ATLAS Open Data', transform=main_axes.transAxes, fontsize=13)
    main_axes.text(0.05, 0.88, 'for education', transform=main_axes.transAxes, style='italic', fontsize=8)
    main_axes.text(0.05, 0.82, f'$\sqrt{{s}}$=13 TeV,$\\int$L dt = {lumi_used} fb$^{{-1}}$', transform=main_axes.transAxes)
    main_axes.text(0.05, 0.76, r'$H \rightarrow ZZ^* \rightarrow 4\ell$', transform=main_axes.transAxes)

    # Draw the legend
    main_axes.legend(frameon=False)

    # Display the plot in Streamlit
    st.pyplot(fig)

def process_and_plot_higgs_data(mc_samples,lumi):
    # Check if there is already processed data from the previous cut
    if st.session_state.invariant_mass_calculated:
        # Retrieve the already filtered data
        data = st.session_state.ALL_DATA['data']

        # Set binning and data variables
        xmin, xmax = 80, 250  # GeV for the four-lepton system
        step_size = 5  # GeV
        bin_edges = np.arange(start=xmin, stop=xmax + step_size, step=step_size)
        bin_centres = np.arange(start=xmin + step_size / 2, stop=xmax + step_size / 2, step=step_size)

        # Convert data['mass'] to NumPy for binning and plotting
        data_x, _ = np.histogram(ak.to_numpy(data['mass']), bins=bin_edges)
        data_x_errors = np.sqrt(data_x)  # Example errors assuming Poisson statistics

        # Call the function to plot the four-lepton invariant mass with MC
        plot_higgs(bin_centres, bin_edges, data_x, data_x_errors, mc_samples, xmin, xmax, step_size, lumi)

    else:
        st.write("No data available. Please run the initial cut first.")