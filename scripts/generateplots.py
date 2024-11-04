import matplotlib.pyplot as plt
import uproot
import awkward as ak
import numpy as np

# Function to format large numbers with K, M, etc., and round to 3 significant figures
def format_numbers(value):
    if abs(value) >= 1e6:
        return f"{value/1e6:.3g}M"
    elif abs(value) >= 1e3:
        return f"{value/1e3:.3g}K"
    else:
        return f"{value:.3g}"

# Define plot functions for the nleptons and charge-flavor data
# Define plot functions for the nleptons and charge-flavor data
def generate_nleptons(theme, file_name, lepton_counts):
    # Set up the counts for 2, 3, and 4 leptons directly
    filtered_counts = [lepton_counts.get(2, 0), lepton_counts.get(3, 0), lepton_counts.get(4, 0)]

    # Set theme properties
    if theme == 'dark':
        plt.style.use('dark_background')
        font_color = 'white'
    else:
        plt.style.use('default')
        font_color = 'black'

    # Plot histogram
    plt.figure(figsize=(8, 6))
    bars = plt.bar([2, 3, 4], filtered_counts, color=["#00A08A", "#F2AD00", "#F98400"], edgecolor='black', log=True)
    plt.xticks([2, 3, 4])
    plt.xlabel('Number of Leptons', color=font_color, fontsize=14)
    plt.ylabel('Event Count (log scale)', color=font_color, fontsize=14)

    # Display event count on each bar
    for bar, count in zip(bars, filtered_counts):
        plt.text(bar.get_x() + bar.get_width() / 2, count, format_numbers(count), ha='center', va='bottom', color=font_color, fontsize=12)

    plt.savefig(file_name, bbox_inches='tight', transparent=True)
    plt.close()

def generate_barplot(theme, file_name, flavor_charge_data):
    # Set theme-specific properties
    if theme == 'dark':
        plt.style.use('dark_background')
        colors = ['#FF0000', '#5BBCD6']  # Colors for + and - charges
        font_color = 'white'
    else:
        plt.style.use('default')
        colors = ['#FF0000', '#5BBCD6']  # Colors for + and - charges
        font_color = 'black'

    # Data for plotting
    categories = ['e', 'mu']
    counts_positive = [flavor_charge_data[0], flavor_charge_data[2]]  # e+ and mu+
    counts_negative = [flavor_charge_data[1], flavor_charge_data[3]]  # e- and mu-

    # Set up positions for grouped bars
    x = np.arange(len(categories))  # Label locations
    bar_width = 0.35  # Width of each bar

    # Plot the grouped bars
    plt.figure(figsize=(8, 6))
    bars_positive = plt.bar(x - bar_width/2, counts_positive, bar_width, label='+', color=colors[0], edgecolor='black')
    bars_negative = plt.bar(x + bar_width/2, counts_negative, bar_width, label='-', color=colors[1], edgecolor='black')

    # Extend the x-axis limits to add space for the legend
    plt.xlim(-0.5, len(categories) - 0.5)

    # Set labels and title
    plt.xlabel('Flavor', color=font_color, fontsize=14)
    plt.ylabel('Lepton Count', color=font_color, fontsize=14)
    plt.title('Lepton Flavor and Charge Distribution', color=font_color, fontsize=16)

    # Add custom x-axis labels for grouped categories
    plt.xticks(x, categories, color=font_color, fontsize=12)

    # Position the legend inside the plot but to the right side
    plt.legend(title='Charge', loc='upper right')

    # Display the number of events over each bar
    for bars, counts in zip([bars_positive, bars_negative], [counts_positive, counts_negative]):
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                     format_numbers(count), ha='center', va='bottom', color=font_color, fontsize=12)

    # Save plot as PNG
    plt.savefig(file_name, bbox_inches='tight', transparent=True)
    plt.close()

# Data path and variables
path = "2to4lep/"
variables = ["lep_type", "lep_charge"]
sample_data = ['data15_periodD.root', 'data15_periodE.root', 'data15_periodF.root',
               'data15_periodG.root', 'data15_periodH.root', 'data15_periodJ.root',
               'data16_PeriodI.root', 'data16_periodA.root', 'data16_periodB.root',
               'data16_periodC.root', 'data16_periodD.root', 'data16_periodE.root',
               'data16_periodF.root', 'data16_periodG.root', 'data16_periodK.root', 
               'data16_periodL.root']

# Initialize counters
lepton_counts = {2: 0, 3: 0, 4: 0}  # For 2, 3, and 4 leptons per event
flavor_charge_data = [0, 0, 0, 0]    # [e+, e-, mu+, mu-]

# Process data in chunks
for val in sample_data:
    print(f'Processing {val}')
    fileString = path + 'Data/' + val

    with uproot.open(fileString + ":analysis") as t:
        tree = t

        # Process each chunk independently
        for data in tree.iterate(variables, library="ak", step_size="100MB"):
            num_leptons = ak.num(data['lep_type'])

            # Update lepton counts directly for histogram
            for count in num_leptons:
                if count in lepton_counts:
                    lepton_counts[count] += 1

            # Update flavor and charge counts directly for charge-flavor plot
            for event_lep_types, event_lep_charges in zip(data['lep_type'], data['lep_charge']):
                for lepton, charge in zip(event_lep_types, event_lep_charges):
                    if lepton == 11 and charge == 1:
                        flavor_charge_data[0] += 1  # e+
                    elif lepton == 11 and charge == -1:
                        flavor_charge_data[1] += 1  # e-
                    elif lepton == 13 and charge == 1:
                        flavor_charge_data[2] += 1  # mu+
                    elif lepton == 13 and charge == -1:
                        flavor_charge_data[3] += 1  # mu-

# Generate plots if data exists
if sum(lepton_counts.values()) > 0:
    print("Data processed successfully!")
    generate_nleptons('light', 'lepton_plot_light.png', lepton_counts)
    generate_nleptons('dark', 'lepton_plot_dark.png', lepton_counts)
    generate_barplot('light', 'lepton_barplot_light.png', flavor_charge_data)
    generate_barplot('dark', 'lepton_barplot_dark.png', flavor_charge_data)
else:
    print("No data available.")