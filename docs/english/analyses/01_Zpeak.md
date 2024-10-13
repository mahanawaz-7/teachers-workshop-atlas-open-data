# $Z^0$ decays: finding the $Z^0$ boson mass!

> The following analysis is searching for events where one (or two) [$Z^0$ bosons](https://en.wikipedia.org/wiki/W_and_Z_bosons) decay to two (or four) leptons of same flavour and opposite charge.

> [!NOTE]
For an introduction to the ideas behind $Z^0$ finding, click [here](Events/ZPath.pdf)
> [!END]

As you might recall, leptons can be either electrons or muons, or their antiparticles. **Flavour** just means whether a particle is an (anti)electron or a (anti)muon. We know the $Z^0$ boson has charge zero, so, to conserve charge, the two leptons to which a single $Z^0$ decays must have **opposite charges**.

We also say that electron number and muon number must be conserved in this reaction.

* Electrons and antielectrons (positrons) have $+1$ and $-1$ respectively as their electron numbers, and have zero muon number.
* Muons and antimuons have $+1$ and $-1$ respectively as their muon numbers, and have zero electron number.
* Z^0$ has zero electron number and muon number.

Therefore, we see that if the $Z^0$ decays to two leptons, **they must be the same flavour**. 

We will look at the two-lepton decay first, and then you will have a go with the four-lepton case. First, though, we need to think about how we talk about decays in particle physcis.

## Feynman diagrams and Lorentz vectors

We show decays with a [Feynman diagram](https://en.wikipedia.org/wiki/Feynman_diagram), which (for our purposes) we can think of a diagram of the interaction itself, where time goes from left to right. This is not strictly true, but it will suffice for now.

Each particle is a single line, and you can think of the vertical axis as space, so here we have an electron $e^-$ and its antiparticle, a positron, $e^+$, moving towards each other in space, annihilating each other, producing a photon ($\gamma$) and then that photon decays to two muons.

<CENTER><img src="./images/electronpositronannihilation.png" style="width:50%"></CENTER>


You may have noticed that the arrow for the positron is the wrong way round for the process which we have just described. By convention, the arrow for an antiparticle is reversed. (If you really want to know, it's because an antiparticle can be thought of as a particle moving backwards in time - something which we will not go into here).

Now, we say that energy and momentum must be conserved at each vertex in the Feynman diagram. $\vec{p}^\mathrm{tot}_\mathrm{before} = \vec{p}^\mathrm{tot}_\mathrm{after}$, and $E^\mathrm{tot}_\mathrm{before} =E^\mathrm{tot}_\mathrm{after}$.

A concise way of writing that is with a **Lorentz vector**, or 4-vector, which neatly packages together energy and momentum.

$$P^\mu = (E/c, \vec{p}) = (E/c, p_x, p_y, p_z)$$

The $\mu$ is just an arbitrary index, starting at zero, so $P^0 = E/c$, $P^1 = p_1 = p_x$, $P^2 = p_2 = p_y$, $P^3 = p_3 = p_z$. However, we make sure to write it to make it clear that this is no ordinary spatial vector that we're dealing with.

We can add and subtract these four-vectors like any other vector with four components:

$$P^\nu_{e^+} + P^\nu_{e^-} = (E_{e^+} + E_{e^-}, \vec{p}_{e^+} + \vec{p}_{e^-}) = P^\nu_\mathrm{tot}$$

Since all of its components must be conserved, $P^\mu_\mathrm{before} = P^\mu_\mathrm{after}$ at every vertex.

For the electron-positron annihilation above, conserving 4-momentum at each vertex, we have:

$$P^\nu_{e^+} + P^\nu_{e^-} = P^\nu_\gamma\text{, and } P^\nu_\gamma =  P^\nu_{\mu^+} +  P^\nu_{\mu^-}$$

More interestingly, if you remember the most famous equation in Physics, $E=mc^2$. That's only true if an object is stationary. If it's not, you have $E^2 = m^2 c^4 + p^2 c^2$. The $m$ in this is called its invariant mass. Clearly, you can quite easily construct $m$ from the components of the 4-vector. 

$$m = \frac{1}{c^2}\sqrt{E^2 - p^2 c^2}$$

###  Units

One last thing - we can just pick a system of units in which $c = 1$. We basically do this by redefining what our SI units are. Imagine that we measured distances in pirate-wizards, which we define to be equal to $299 792 458$ metres. Let's keep measuring times in seconds, though. You, then are about $6\times 10^{-9}$ pirate-wizards tall.

You may have noticed the specific value we picked for a pirate-wizard. 

> [!WARNING]
What does that mean the speed of light is, measured in our new unit system?
> [!END]

<details>
    <summary>Answer: </summary>
    It's exactly $1$ pirate-wizard per second!
</details>

Let's then define the unit of energy as 1 GeV - one gigaelectronvolt. What does that make our unit of mass? Now, we know that the units still have to match up dimensionally, and we know that $1 kg = 1 Joule /c^2$, so let's measure mass in $eV /c^2$. Similarly, let's measure momentum in $eV/c$.

So, we can measure some particle A to have a mass of $3 GeV/c^2$, an energy of $5 GeV/c^2$, and a momentum of $4 GeV/c$. The advantage of setting $c=1$ is that we can throw out all of those extra $c$s. That means we can measure everything in units  of $GeV$! So, our particle A just has $m=3$, $E=5$, and $p=4$. Of course, you can't do dimensional analysis any more, but it makes a lot of things easier - trust me. For one thing, our mass equation turns out to be pretty simple: $m = \sqrt{E^2 - p^2}$. 

**Check if particle A satisfies this!**


## How to use TLorentzVectors in Python
 
Since we're using code, we're going to have a pretty simple function that takes our Lorentz Vector and spits out the rest mass of that Lorentz vector.

Thankfully, the dirty work has been done for you already. If you have a TLorentzVector variable called `particle1`, and you want its invariant mass, just do this:

`particle1.M()`


First of all - like we did it in the first notebook - uproot is imported to read the files in the .root data format, and to give us the relevant libraries.

```python
import uproot
```

We'll also be using the python module `numpy` regularly throughout this notebook - let's import this too.

```python
import numpy as np
```

We've written a module that generates Lorentz vectors, so let's import it.

```python
from TLorentzVector import TLorentzVector
```

Now, let's declare two TLorentzVectors. We do this by declaring two variables, and then saying that each one is a `TLorentzVector` from the library `ROOT`.

```python
particle1 = TLorentzVector()
particle2 = TLorentzVector()
```

Of course, they're just empty vectors at the moment. Let's set them with values. Notice the way this is written, with the E coming last.

_Try editing the code to print the energy $E$._

```python
particle1.SetPxPyPzE(0, 0, 0, 1)
print(particle1.Px())
print(particle1.Py())
print(particle1.Pz())
print(particle1.E())
####
particle1_energy = 0 #FIX ME!
print("The energy is ", particle1_energy, "MeV") 
particle1_mass = 0 #FIX ME!
print("The energy is ", particle1_mass, "MeV/c^2")
```

As a reminder from your event displays, the detector gives us momentum in an odd way. Place yourself in spherical coordinates, $(r,\theta,\phi)$, with the collision point at $r=0$, and the direction of the beam (the beam axis) along $\theta =0$.

<figure>
  <center>  <img src="images/CMSangles.png" alt="image missing" style="height: 300px" />
     <figcaption>Quantities $\theta$, $\eta$ and $\phi$ in the ATLAS detector.</figcaption> </center>
</figure>

In our data files, we get given the following three quantities for each lepton.

* $p_T$: the amount of momentum perpendicular to the direction of the beam, called the **transverse momentum**.
* $\eta$: the rapidity, which is a function of the polar angle $\theta$: 
$$
\eta = -\ln(\tan(\frac{\theta}{2}))
$$
* $\phi$: the azimuthal angle - direction of that perpendicular component of momentum (in radians, of course). This is just like the azimuthal angle in spherical coordinates.

<div class="alert alert-warning">Does this uniquely determine (three-)momentum?.</div>


<details>
    <summary>Answer: </summary>
    Yes! We are measuring a three-dimensional momentum, and have been given three mutually-exclusive ('orthogonal') coordinates.
</details>


So, we can also define the components of $P^\mu = (E, \vec{p})$ like this, using the function `.SetPtEtaPhiE(pt, eta, phi, E)`.

So, if $p_T = 1 GeV$, the rapidity $\eta = 1.0$, and the transverse component of momentum came off at an azimuthal angle $\phi = \pi/2$, and its overall energy is $5 GeV$, we can build the Lorentz vector as follows.

```python
from numpy import pi # We need to import the value of pi from the numpy library
particle2.SetPtEtaPhiE(1, 1, pi/2, 5)
particle2.M()
```

Finally, you can add four-vectors in Python just like you can mathematically. if you want to define $P^\mu_3 = P^\mu_1 + P^\mu_2$, it is as easy as `particle 3 = particle1 + particle2`.

```python
# Add the particle 1 and particle2 four-vectors together, 
# and print out the invariant mass of the two-particle system




```

## Decays

Back to the decays, then.

We want to find $Z^0$ bosons, but they don't live long enough to actually see with the detector itself. Instead, we have to **reconstruct** them from their decay products. We don't particularly mind where the $Z^0$s themselves come from. All you need to know here is that each time the LHC smashes two protons together, they produce lots and lots of particles, some of which are $Z^0$s.


From theory, we know that there are two main decay routes. The first is to two leptons, and the second is to four leptons.

### To two leptons

The first option is that a random Z that emerges from the collision aftermath in the LHC (we don't care how) can decay directly to two leptons of the same type, but opposite charge. This means an electron and an antielectron, a muon and an antimuon. The decay happens at the vertex below, marked by a dot. We denote a lepton by the letter $\ell$. Conventionally, antiparticles are shown with a bar on top, so an antilepton is $\bar{\ell}$.

<CENTER><img src="./images/Z_to_ll.png" style="width:30%"></CENTER>

*Using what you know above, write down the equation of conservation of the energy-momentum four-vector for the above decay.*

The ATLAS detector can measure the momentum and energy of leptons coming out of decays, and you can access that information quite simply. It also measures the charge and flavour of each lepton (whether its a muon/antimuon, or electron/antielectron).

We mentioned earlier that each smash makes lots of particles. That's true - in fact, it makes so many that we can't actually store all the records of what happened, even on some of the biggest data storage facilities in the world. 

Instead, we use what is called a trigger. The trigger here was us seeing **exactly one high energy lepton** and **one jet with a large radius** (don't worry about what that is for now), so all of our data will contain at least those two things, as well as a bunch of other particles.

<!-- #endregion -->

Next we have to open the data that we want to analyze. As described earlier, the data is stored in a *.root file. We can use a python library called uproot to access the data. Below is an example of how to open a *.root file using uproot

```python
## 2 lepton file
f = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_361106.Zee.1largeRjet1lep.root") ## 13 TeV sam
```

We can inspect the contents of a file by using the method keys()

```python
f.keys()
```

We see that we have an object called 'mini'. We can obtain information about the object in the file and its type by using the method classnames()

```python
f.classnames()
```

We see that the object called mini is a TTree type. A TTree is simply columns of data stored in the .root format. Each column of data can represent a different physical quantity of a particle. For instance, its charge, energy, momentum etc.

Now we know what data the file contains, in future we can quickly access that data. We want to access the mini data. This can be done by executing the command below


```python
events = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_361106.Zee.1largeRjet1lep.root:mini")
```

Let's look at contents of the TTree. Essentially all the columns in the TTree called mini

```python
events.keys()
```

We see columns such as lep_pt and lep_E. This is the transverse momentum and energy respectively of leptons. We can use the .arrays method to access events with just the columns we specify.

```python
sel_events = events.arrays(["lep_n", "lep_charge", "lep_type", "lep_pt", "lep_eta", "lep_phi", "lep_E"])
```

We want to run over all the data and reconstruct the $Z^0$ boson mass. To do this we will access events using the arrays method again. Let's look at doing this.

First we define a histogram. To do this we can import the python hist library. Once we have done that we can define a histogram. Its name is hist and the x axis is named mass [GeV]. The three initial arguments indicate that this histogram contains 30 bins which fill the gap from 40 to 140.


```python
import hist
from hist import Hist

hist1 = Hist(hist.axis.Regular(30,40,140, label = "Mass (GeV)"))
```

It is now time to fill our above defined histogram with the masses. To do that, we need to reconstruct our $Z^0$ boson Lorentz vector. We do this by narrowing down all our events to those that have two leptons of opposite charge and the same flavour, then building `TLorentzVector`s for each of them, and then adding them together. From your equation above, that would give the Lorentz vector of the parent particle - the $Z^0$ (we hope). Once we have that, the invariant mass can come from `Z0_boson_Lorentz_vector.M()`.

**The process of narrowing down the number of candidates by imposing a condition is called making a cut**.


## Cuts <a name="4."></a>

Why do we make cuts? Remember that there are lots of other particles flying around, and sometimes you'll just have two electrons of the same charge and same flavour, that have nothing to do with each other, that we measure. Obviously, they won't reconstruct to a $Z^0$ boson.

Therefore, we need to not count these events based on that, so we **cut** on the fact that there are two leptons of the same flavour, and then cut again on the fact that those two leptons are oppositely charged.

**You may have spotted an issue here - what if we have two random unassociated electrons of the same flavour and opposite charge? We can't eliminate those.**

One thing you might want to take note of is that the detector gives us energies and momenta in units of $MeV$! This means that when building our LorentzVectors, we have to divide by a thousand, so that our LorentzVector has an overall unit of $GeV$.

> [!NOTE]
Make sure you read through the code - particularly the comments! You'll be doing this yourself shortly.
> [!END]

- Cuts
- T vector
- Invariant mass


The $Z^0$ boson decays through two channels:
- $Z^0 \rightarrow l^+ \; l^-$
- $Z^0 \rightarrow l^+ \; l^- \; + \; l^+ \; l^-$

where $l^+ \; l^-$ is a lepton-antilepton pair with the constituent leptons being of the same family.  This means the options are $e^+ \; e^-$, $\mu^+ \; \mu^-$, $\tau^+ \; \tau^-$.  $\tau$ leptons are rarely produced, so we will generally be looking for $e^+ \; e^-$ and $\mu^+ \; \mu^-$ pairs.

This means we can deduce the following for a *pass event*:
- There must be at least 2 leptons produced by the event - see by observation
- Must be of opposite charge, or equivalently of *unequal charge* (since only two possibilities for charge)
- Must be of the same family - see by specification

```python
# Declare the two TLorentzVectors

leadLepton  = TLorentzVector()
trailLepton = TLorentzVector()

sel_events = events.arrays(["lep_pt", "lep_eta", "lep_phi", "lep_E","lep_charge", "lep_type", "lep_n"])
                  
    
# Now, iterate through each event in the tree!
for event in sel_events:
    # Cut #1: At least 2 leptons in the event. lep_n  is the number of them.
    
    lep_n = event["lep_n"]    
    if lep_n >= 2:
        
        # Cut #2: Leptons with opposite charge.
        #We have a list of charges, each corresponding to a lepton: lep_charges.
        #Clearly, we can't let these be equal
        lep_charge = event["lep_charge"]
        if (lep_charge[0] != lep_charge[1]):
            
            # Cut #3: Leptons of the same family (2 electrons or 2 muons).
            # lep_type gives back a number, which is a code for what kind of lepton it is.
            lep_type = event["lep_type"]
            if ( lep_type[0] == lep_type[1]):
                
                # By now we should only have paricles that look right remaining.
                
                # Let's set the components of a TLorentzVector for each lepton.
                # Notice that the energy and momenta are given in MeV!
                
                lep_pt = event["lep_pt"]
                lep_eta = event["lep_eta"]
                lep_phi = event["lep_phi"]
                lep_E = event["lep_E"]
                
                leadLepton.SetPtEtaPhiE(lep_pt[0]/1000., lep_eta[0], lep_phi[0], lep_E[0]/1000.)
                trailLepton.SetPtEtaPhiE(lep_pt[1]/1000., lep_eta[1], lep_phi[1], lep_E[1]/1000.)
                
                # Now, reconstruct the Z0 boson Lorentz vector! 
                # Remember, we can add them just like normal vectors.
                Z0_boson = leadLepton + trailLepton
                
                # Put this particular value into the histogram.
                hist1.fill(Z0_boson.M())
    
```

After filling the histogram we want to see the results of the analysis. We import `matplotlib` and get plotting!

```python
import matplotlib.pyplot as plt

hist1.plot(histtype = "fill")
plt.show()
```

**Done**

<div class="alert alert-success">Well done!

If everything went well, you have just reconstructed the $Z^0$ boson!</div>

<div class="alert alert-warning">Interpret this graph - what is the mass of this boson?</div>
<br>
<details>
    <summary>Answer: </summary>
        That's right - 90 GeV!
</details>

## Optional extra exercises / 'Do your own project' ideas  <a name="5."></a>


<div class="alert alert-info"> When completing these execises, it is recommended to copy/paste any code you're reusing from above into new cells, to keep the example available for reference.
<br>
    
New cells can be added above using `esc` + `a`, below using `esc` + `b`, or using the `Insert` tab at the top of the page.</div> 


a) In the exercise above we include all types of leptons (electrons and muons) in our invariant mass histogram. Would this distribution look different if was only electrons, or only muons?

Create two different histograms, one with only pairs of electrons, and one with only pairs of muons. 

<br>
<details>
    <summary>Hint 1</summary>
    The value of the variable lep_type is 0 for electrons and 1 for muons. In the event loop, after the event has passed all the selections, you can assign the array of lep_type values for that event to a variable e.g.
    
        lep_type = event["lep_type"]
</details>
<br>
<details>
    <summary>Hint 2</summary>
    You'll need to book and fill two seperate histograms - one for each type of lepton
</details>
<br>
<details>
    <summary>Hint 3</summary>
    Remember if/elif/else statements? Just before filling your histograms in the event loop,
       
        if (lep_type[0]==11) & (lep_type[1]==11):
            #Fill your electron histogram
        elif (lep_type[0]==13) & (lep_type[1]==13):
            #Fill your muon histogram
</details>

Draw both histograms and compare. 
> [!WARNING]
What does this tell us about the underlying physics?
> [!END]

b) The ATLAS detector can de divided into two regions based on __pseudorapidity__ $\eta$, as described in the section ['How to use TLorentzVectors in Python'](#2.). 

These are: 
- The _central_ region |$\eta$| < 2.47, which is made up of the ATLAS _barrell_
- The _forward_ region |$\eta$| > 2.47, which is made up of the ATLAS _endcap_

Create two different histograms: One using only lepton pairs with central (small) pseudorapidities and one using only those with forward (large) pseduorapidities.

<br>
<details>
    <summary>Hint 1</summary>
    You can get the absolute values with the function np.absolute() from the _numpy_ module
</details>
<br>
<details>
    <summary>Hint 2</summary>
    You'll need to book and fill two seperate histograms - one for each |$\eta$| category
</details>
<br>
<details>
    <summary>Hint 3</summary>
    Remember if/elif/else statements? Just before filling your histograms in the event loop,
       
        if (np.absolute(lep_eta[0])< 2.47) & (np.absolute(lep_eta[0])< 2.47):
            #Fill your central pseudorapidies histogram
        elif (np.absolute(lep_eta[0])> 2.47) & (np.absolute(lep_eta[0])> 2.47):
            #Fill your forward rapidities histogram
</details>


Draw your two new histograms.  

<div class="alert alert-warning">How does the pseudorapidity of the leptons that are detected in the ATLAS detector affect the invariant mass distribution?What could be the reason for this?</div>

<br>
<details>
    <summary>Hint 1</summary>
    Narrower peaks $\rightarrow$ better momentum resolution (how accurately the momentum is measured)
</details>
<br>
<details>
    <summary>Hint 2</summary>
    When particles pass through the detector, the interact with it and lose some of their energy, which can mess up the measurement of their momentum a little.
</details>
<br>
<details>
    <summary>Hint 3</summary>
    Which set of particles passes through more of the detector?
</details>
<!-- #endregion -->

#### c) Extra - Fitting to histograms!


> [!CAUTION]
This is an advanced extra prompt - feel free to skip it if you want to!
> [!END]

To get information about the mass and lifetime of the detected resonance, a function that describes the distribution of the invariant masses must be fitted to the values of the histogram. In our case the values follow a Breit-Wigner distribution:

$$
N(E) = \frac{K}{(E-M)^2 + \frac{\Gamma^2}{4}},
$$

where $E$ is the energy, $M$ the maximum of the distribution (equals to the mass of the particle that is detected in the resonance), $\Gamma$ the full width at half maximum (FWHM) or the decay width of the distribution and $K$ a constant.

The Breit-Wigner distribution can also be expressed in the following form:

$$
\frac{ \frac{2\sqrt{2}M\Gamma\sqrt{M^2(M^2+\Gamma^2)} }{\pi\sqrt{M^2+\sqrt{M^2(M^2+\Gamma^2)}}} }{(E^2-M^2)^2 + M^2\Gamma^2},
$$

where the constant $K$ is written open.

The decay width $\Gamma$ and the lifetime $\tau$ of the particle detected in the resonance are related in the following way:

$$
\Gamma \equiv \frac{\hbar}{\tau},
$$

where $\hbar$ is the reduced Planck's constant.

1) In your event loop, add a new cut on the lepton pair inavriant mass, to limiting the histogram values to be close to the peak, e.g. between 70 GeV and 110 GeV


2) Save the number of events per bin, and the bin values to arrays using inbuilt functions from the python `hist` module:

```python
y = hist1.counts()
x = hist1.values()
```
3) Define the function that describes Breit-Wigner distribution for the fit. 

```python
def breitwigner(E, gamma, M, a, b, A):
    return a*E+b+A*( (2*np.sqrt(2)*M*gamma*np.sqrt(M**2*(M**2+gamma**2)))/(np.pi*np.sqrt(M**2+np.sqrt(M**2*(M**2+gamma**2)))) )/((E**2-M**2)**2+M**2*gamma**2)
```

 - E is the energy
 - $\Gamma$ is the decay width
 - M is the maximum of the distribution
 - a, b and A different parameters that are used for noticing the effect of the background events for the fit.


Assign the initial values for the optimization to a list in the following order:
i) $\Gamma$ (the full width at half maximum (FWHM) of the distribution)

ii) M (the maximum of the distribution)

iii) a (the slope that is used for noticing the effect of the background)

iv) b (the y intercept that is used for noticing the effect of the background)

v) A (the "height" of the Breit-Wigner distribution)

```python
initials = [GUESS_FOR_GAMMA_FROM_HIST, GUESS_FOR_M_FROM_HIST, -2, 200, 13000]
```

4) Import the module that is used in the optimization, run the optimization and calculate the uncertainties of the optimized parameters.

```python
from scipy.optimize import curve_fit
best, covariance = curve_fit(breitwigner, x, y, p0=initials, sigma=np.sqrt(y))
error = np.sqrt(np.diag(covariance))
```

5) Print the values and uncertainties that are got from the optimization.

```python
print("The values and the uncertainties from the optimization")
print("")
first = "The value of the decay width (gamma) = {} +- {}".format(best[0], error[0])
second = "The value of the maximum of the distribution (M) = {} +- {}".format(best[1], error[1])
third = "a = {} +- {}".format(best[2], error[2])
fourth = "b = {} +- {}".format(best[3], error[3])
fifth = "A = {} +- {}".format(best[4], error[4])
print(first)
print(second)
print(third)
print(fourth)
print(fifth)
```

6) Plot your histograms using the regular `hist1.plot()` command. Then plot your fitted function using:

```python
plt.plot(x, breitwigner(x, *best), 'r-', label='gamma = {}, M = {}'.format(best[0], best[1]))
plt.xlabel('Invariant mass [GeV]')
plt.ylabel('Number of event')
plt.title('The Breit-Wigner fit')
plt.legend()
plt.show()
```

__Note:__ The even more correct way for doing the fit and getting the values and the uncertainties from it would be to iterate the fit several times. In the iteration a next step would take initial guesses from the previous fit.


The width of the decay (called $\Gamma$) and the lifetime $\tau$ of the particle detected in the resonance are related in the following way:

$$
\Gamma \equiv \frac{\hbar}{\tau},
$$

where $\hbar$ is the reduced Planck's constant and is equal to $6.58 \times 10^{-16}$ $\rm{eV s}$.

> [!WARNING] 
Q1: Calculate the lifetime $\tau$ of the Z boson with the uncertainty by using the fit.

Q2: Compare the calculated value to the known lifetime of the Z. What do you notice?
> [!END]


> [!TIP]
__Congratulations!__ You've looked at real particle collision data and discovered the $Z^0$ boson, a feat we didn't accomplish at CERN until 1983! To hone your skills and play some more with the $Z^0$ boson, move on to Notebook 5.
> [!END]
