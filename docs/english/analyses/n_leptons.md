## Number of Leptons in the Final State
In particle colliders, when a particle is produced, it can decay immediately to other particles, which are detected and analyzed. By identifying all the particles in the final state, we can infer what particles were initially created during the collision. One example is the number of leptons in the final state, as different processes produce different numbers of leptons.

Below is a [Feynman diagram](https://cds.cern.ch/record/2791333/files/Feynman%20Diagrams%20-%20ATLAS%20Physics%20Cheat%20Sheet%20in%20Spanish%20%7C%20Diagramas%20de%20Feynman.pdf) showing a typical process that results in a final state with two leptons:

![Z boson decay into two leptons](images/Z_decay_{theme}.png)

More complex decays may involve more leptons in the final state:

![Higgs boson decay into Z bosons and leptons](images/higgs4l_decay_{theme}.png)

Below you can see the count of number of leptons in the whole dataset. You can see that, in general, it is more common to have fewer leptons in an event:

![Lepton counts](images/lepton_plot_{theme}_{lumi}.png)

Study the diagrams and the data, and select how many leptons you expect to observe in your final state depending on the analysis you are doing – finding the Z boson or the Higgs boson.

> [!CAUTION] 
You are about to select the number of leptons you want in your data. However, it's important to note that we’ve added additional criteria to ensure the quality of these leptons:
- **Isolation:** Each lepton must be isolated, meaning it isn’t clustered with other particles. This ensures that we're focusing on leptons that likely originated directly from the particle we’re interested in, rather than from background interactions.
- **Identification Levels:** Leptons must meet specific identification criteria to confirm their type with high confidence. Particle reconstruction is complex, so we have different levels of identification for certainty. For example, muons must pass a medium ID level, while electrons only need to pass a loose ID level, as electrons are easier to detect.
- **Trigger Conditions:** Triggers are criteria set to capture events with certain characteristics, allowing only saving events that we want to analyze. Here, we use electron and muon triggers to select events with significant signals, refining the dataset to increase the chances of observing particles that decay to leptons or muons.

These criteria help "clean" the data, improving our chances of observing particles like the Z and Higgs bosons.
> [!END]