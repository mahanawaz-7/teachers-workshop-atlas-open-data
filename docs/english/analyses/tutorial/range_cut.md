## Range Cut: Selecting Events by Leading Lepton Energy
In particle physics, the energy of the **leading lepton** — the lepton with the highest energy in an event — is an important property. It provides insights into the interactions and decays occurring in the analyzed events. Higher-energy leading leptons can indicate the presence of heavier particles, such as the Higgs boson, and their behavior helps identify the nature of the event. By selecting events based on the leading lepton energy, we can reduce background noise and focus on meaningful signals.

In this step, you will apply a range cut to filter the dataset based on the leading lepton energy. This involves selecting a minimum and maximum energy value (measured in giga-electronvolts, or GeV) to isolate events where the leading lepton's energy falls within this range.

Use the slider below to specify the energy range. For example: A range of 20 to 150 GeV retains events where the leading lepton energy is higher than 20 GeV and lower than 150 GeV

The dataset will dynamically update as you adjust the range, providing a clear view of how this filter refines the dataset. To verify the range cut, inspect the `LeadingLeptonEnergy` column in the dataset to ensure all values are within the selected range.