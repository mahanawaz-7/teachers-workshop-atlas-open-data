# Intro to histogramming
In particle physics, we use so many events to make our measurements that looking at the events by hand would be very impractical - instead, we use computer code to do the looking for us.

This resource will walk you through some basic computing techniques commonly used in high energy physics (HEP) analyses. You will learn how to:

1. Interact with ATLAS data files
2. Create a histogram for displaying data
3. Fill your histogram
4. Draw your histogram
5. Normalise your histogram
    
We will be showing you examples of these techniques to produce a plot with the __number of leptons__ in each event in a set of 13 TeV Z boson data. At the same time, you will be following along to produce your own plot with the __number of jets__ in each event in a set of 8 TeV W and Z boson data. TeV stands for 'Tera-electron-volt' and is a unit of energy we use in particle physics - we will learn more about the units we use in particle physics in the next notebook!

> [!NOTE]  
> Before you get into your histogramming and are introduced to Z invariant mass, make sure you review the fundamentals of particle physics and the Standard Model by watching [this](https://youtu.be/hmM-ic4Wh68) RAL video by Dr Emmanuel Olaiya.
> [!END]

## Step 0: What to load 

The software we will use to analyse our ATLAS data is called __uproot__ and __hist__. Using `uproot`, we are able to process large datasets, do statistical analyses, and visualise our data using __hist__. The data is stored in a format called .root

```python
#Import the uproot library
import uproot

#Here you could also import any other python libraries you would like to use
import matplotlib.pyplot as plt
import numpy as np
```

## Step 1: Working with .root files

<!-- #region -->
Next we have to open the data files that we want to analyze. 

As mentioned above, the format for storing physics data - is a _[something].root_ file. For each event in the dataset we could have many particles, and for each particle, there are several __variables__ we measure (e.g. energy, momentum, charge). The structure of a _*.root_ file is as follows:


- A _.root_ file stores and keeps track of all this information in a container called a __TTree__. 
- Inside the TTree, each variable that we measure are stored separately in containers called __branches__. 
- Inside each branch, the measurement of that variable for each event is stored.
<!-- #endregion -->

<CENTER><img src="./images/root_struct.png" style="width:70%"></CENTER>


Lets load our _.root_ file using `uproot`'s `uproot.open()` function. The __argument__ inside the brackets tells uproot where to look for the file.

```python
f = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_361106.Zee.1largeRjet1lep.root") ## 13 TeV sample
#f = uproot.open("https://atlas-opendata.web.cern.ch/release/2016/MC/mc_105987.WZ.root") ## 8 TeV sample
```

> [!TIP]
> You could uncomment one of the other lines to repeat the analysis we will do below for a different dataset (remember to comment out the top line first).
> [!END]

> [!NOTE]  
> If you are curious about where the files above come from, check out the instructions for finding the ATLAS Open Data [here](FindingOpenData.pdf)
> [!END]


Next, to inspect the contents of a _.root_ file, we use the `.keys()` function.

```python
f.keys()
```

We can see what this object 'mini' is using the `.classnames()` function.

```python
f.classnames()
```

This means *mini* is a TTree object and should contain all the data we need.  To load the TTree data directly, we can select it using the below code.

```python
my_tree = f["mini"]
```

Alternatively, we can change our file loading code so it specifies the TTree file *mini*.

```python
my_tree = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_361106.Zee.1largeRjet1lep.root:mini")
```

The `.show()` function allows us to see the full contents of our TTree.

```python
my_tree.show()
```

We see the names of all the different quantities stored. Rather than use the word name (written at the top of the table), we use the word branch. Let's look at an individual branch in this TTree to see its form. We specify what branch we want to look at ("lep_eta") and the type of array we want to output ("np" which is short for numpy array)

```python
lep_eta = my_tree["lep_eta"].array(library="np")
lep_eta
```

In effect, this is a 2D array containing 2 elements: an array of values, and the data type of the array.  It is this method of storing values that allows an array to be 'jagged' - that is, having each row be a different length - without becoming an issue for array manipulation.


We can see how many events are stored in the tree by looking at the length of the array using the len function

```python
len(lep_eta)
```

### Over to you


__1)__ __Replace the ###'s in the cell below__ to open the _*.root_ data file `" https://atlas-opendata.web.cern.ch/release/2016/MC/mc_105987.WZ.root"`


<details>
    <summary>Click here for hint 1: </summary>
    
    What function did we use above to open a .root file?
</details>

```python
my_file = ###

```

<details>
    <summary>Answer: </summary>

    my_file = uproot.open("https://atlas-opendata.web.cern.ch/release/2016/MC/mc_105987.WZ.root")
</details>


__2)__ Load the tree named "mini" stored in the _.*root_ data file. Print the number of events in this tree.


<details>
    <summary>Click here for hint 1: </summary>
    All data is stored in the TTree 'mini'.
</details>


<details>
    <summary>Click here for hint 2: </summary>
    Pick a branch (name) and output it as an array .
</details>


<details>
    <summary>Click here for hint 3: </summary>
    Look at the length of the array
</details>

```python
my_tree = my_file[###]
eventNumber = my_tree[###].array(###)
print(###)

```

<details>
    <summary>Answer: </summary>
        
    my_tree = my_file["mini"]
    eventNumber = my_tree["eventNumber"].array(library="np")
    len(eventNumber)
</details>


__3)__ We will also need to create variables for the maximum number of jets and the minimum number of jets seen by a single event in this dataset for later.


<details>
    <summary>Click here for hint 1: </summary>
    The object you need is called "jet_n". Get an array which is the jet_n for each event
</details>


<details>
    <summary>Click here for hint 2: </summary>
    Numpy has two functions, .min() and .max(), that return the minimum and maximum values of an array.
</details>


<details>
    <summary>Click here for hint 3: </summary>
    Remember the first event is [0]!
</details>

```python
import numpy as np

jet_n = my_tree[###].array(###)
minimum = np.min(###)
maximum = np.max(###)
print("Minimum number of jets:", ###)
print("Maximum number of jets;", ###)
      
#Peek inside the first event using list indexing
jet_n_Event1 = jet_n[#] 
print("Number of jets in Event 1:", ###)
```

<details>
    <summary>Answer: </summary>
        
    import numpy as np

    jet_n = my_tree["jet_n"].array(library="np")
    minimum = np.min(jet_n)
    maximum = np.max(jet_n)  
    print("Minimum number of jets:", minimum)
    print("Maximum number of jets;", maximum)
    
    jet_n_Event1 = jet_n[0]
    print("Number of jets in Event 1:", jet_n_Event1)
</details>


---


## Step 2: Getting ready to display histograms <a name="2."></a>


Before we can display any histograms, we must import a few modules:
- `hist` is a library that handles the generation and customization of histograms
- `Hist` is a module from `hist` that allows for the generation of a basic histogram

```python
import hist
from hist import Hist
```

Let's generate a regular histogram using `Hist`; we'll use the `hist.axis.Regular()` option, which takes arguments `(bins, lower_lim, upper_lim, label = "axis label")`.  Here, the **bins** of our histogram are 'slices' of the range of values we fill our histogram with.  But what to fill our histogram with?


A simple choice would be the number of leptons, as we can guess the number of bins and both the upper and lower limits fairly easily; the smallest number of leptons would be $0$ and the largest number $4$ - this corresponds to 5 bins ($0,1,2,3,4$), a lower limit of $0$ and an upper limit of $4$.  Let's implement this:

```python
hist1 = Hist(hist.axis.Regular(5, -0.5, 4.5, label = "Number of leptons"))
```

Note the offset of 0.5 in the range arguments. This shifts the bins so they are centred on 0,1,2,3,4 rather than having their leftmost edges on those values, as is the default.


> [!IMPORTANT]  
> We don't expect any output to be printed from this step - all we're doing here is telling python the details of the histogram we're planning to fill.
> [!END]


### Over to you

__4)__ Create a template histogram called "Number of jets" to display your plot.


<details>
    <summary>Click here for hint 1: </summary>
    Use the minimum (-0.5) and maximum number of jets (9.5) for your axis limits.
</details>


<details>
    <summary>Click here for hint 2: </summary>
    Use the maximum number of jets for your bin numbers.
</details>

```python
my_hist = Hist(hist.axis.Regular(###, ###, ###, label = ###))
```

<details>
    <summary>Answer: </summary>
        
    my_hist = Hist(hist.axis.Regular(5, -0.5, 9.5, label = "Number of jets"))
</details>

---

## Step 3: Filling histograms <a name="3."></a>


Now to fill our histogram!  The first step is to extract the number of leptons from our TTree using `uproot`.  We'll want to extract it in the form of a `numpy` array like so:

```python
lep_n = my_tree["lep_n"].array(library="np")
```

This is the data we shall use to fill our histogram using the `.fill()` function from `hist`.  It's very simple:

```python
hist1.fill(lep_n)
```

To properly render our histogram, we'll need to plot it using the `.plot()` function from `hist` and the `plt.show()` function from `matplotlib`.  Let's import `matplotlib` and do exactly this.

```python
hist1.plot()
plt.show()
```

> [!NOTE]  
> In later examples, we'll be more picky about the events we put in our histogram, skipping some events in the tree if they don't meet certain criteria. This is called making cuts.
> [!END]


### Over to you

__5)__ Fill your histogram with the number of jets in each event.


<details>
    <summary>Click here for hint 1: </summary>
        Remember: we've already made a template histogram.
</details>


<details>
    <summary>Click here for hint 2: </summary>
        The data you're after is "jet_n".
</details>

```python
my_hist.fill(###)
my_hist.###
plt.###
  
```

<details>
    <summary>Answer: </summary>
        
    my_hist.fill(jet_n)
    my_hist.plot()
    plt.show()
</details>

---

## Step 4: Drawing histograms <a name="4."></a>


Adding a title to a histogram is fairly easy - you simply pass `plt.title()`.

```python
hist2 = Hist(hist.axis.Regular(5, -0.5, 4.5, label = "Number"))
hist2.fill(lep_n)
hist2.plot()
plt.title("Number of leptons in a 13 TeV dataset")
plt.show()
```

We can also include multiple histograms on the same axis, which is useful if you're trying to look for a particularly elusive particle.  Let's start by accessing the necessary `.root` files.

```python
tr1 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363491.lllv.1largeRjet1lep.root:mini")
lep_n1 = tr1["lep_n"].array(library = "np")
```

```python
tr2 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363492.llvv.1largeRjet1lep.root:mini")
lep_n2 = tr2["lep_n"].array(library = "np")
```

```python
tr3 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363493.lvvv.1largeRjet1lep.root:mini")
lep_n3 = tr3["lep_n"].array(library = "np")
```

Here, the events in question produced leptons and their associated neutrinos.  We're curious as to how many leptons were produced in each event and how these numbers compare, so overlapping our histograms would be preferable. This is a straightforward process. You can fill three separate histograms, and plot them one after the other. Everytime you run `plot()`, it will draw the histogram on top of what is already there. Of course run `plt.show()` to display what you have drawn. Run the cells below as an example.

```python
#Create the histgrams

ax1 = Hist(hist.axis.Regular(5, -0.5, 4.5, label = "Number of leptons"))
ax2 = Hist(hist.axis.Regular(5, -0.5, 4.5, label = "Number of leptons"))
ax3 = Hist(hist.axis.Regular(5, -0.5, 4.5, label = "Number of leptons"))
```

```python
#Fill the histograms

ax1.fill(lep_n1)
ax2.fill(lep_n2)
ax3.fill(lep_n3)
```

```python
#Draw one histogram on top of the other and then display the final plot

ax1.plot()
ax2.plot()
ax3.plot()

plt.show()
```

Rather than overlay the histograms this stacks the bin contents on top of each other. This is for useful when you want to add data. We can simply add the histograms and then plot the sum

```python
histo_sum = ax1+ax2+ax3
histo_sum.plot()
plt.show()
```

We can also use the `.stack()` function from `hist`, to overlay or stack histograms, though we'll need to prepare a little first. 


Let's start with the axis of our template histogram, which will be the same as our previous histogram on lepton numbers.

```python
ax = hist.axis.Regular(5, -0.5, 4.5, flow=False, name = "Number of leptons")
```

Now we need a 'category axis' or `cax`, which operates in a similar manner to a dictionary.  Its $1^{st}$ argument is a list of histogram labels and its $2^{nd}$ argument is a label for the collective axis.  In effect, each histogram label is like a key, linking each histogram to its name, color and position.

```python
cax = hist.axis.StrCategory(["lllv", "llvv", "lvvv"], name = "c")
```

Now to generate our 'stacked' histogram.  `Hist()` actually takes two arguments - the *axis* and the *category axis*.

```python
full_hist = Hist(ax, cax)
```

`.fill()` also takes two arguments - *data* and *category*.  Let's fill for each dataset.

```python
full_hist.fill(lep_n1, c = "lllv")
full_hist.fill(lep_n2, c = "llvv")
full_hist.fill(lep_n3, c = "lvvv")
```

Yep, this is impossible to read - particularly as we have no idea which monochrome shade represents which dataset! Lets use the stack method and specify the name of the  label `"c"`. This will overlay this histograms.

```python
s = full_hist.stack("c")
s.plot()
```

This looks the same as the output from our previous overlay method, as it should! This plot is slightly more discernible, but we still don't know which histogram is which!  We should add  a title and a legend to properly render our stacked histogram, as well as fill it in so the coloured regions are more visible.

```python
s = full_hist.stack("c")
s.plot(histtype = "fill")
plt.title("Lepton counts per event for multiple datasets")
plt.legend()
plt.show()
```

Here, we've used the condition `histtype = "fill"` when plotting our histogram.


We can 'stack' this histograms so that the bin contents are added. We can do this by setting the stack option to True as follows 

```python
s.plot(stack=True, histtype = "fill")
plt.title("Lepton counts per event for multiple datasets")
plt.legend()
plt.show()
```

Again the bin contents look the same as our previous method of just adding the histograms


Below is an example showing the steps from opening a root file, filling a histogram and plotting the data

```python
f = uproot.open("https://atlas-opendata.web.cern.ch/release/2016/MC/mc_105987.WZ.root")
tree = f["mini"]
lep_n = tree["lep_n"].array(library="np")
lep_n

hist_n = Hist(hist.axis.Regular(5, -0.5, 4.5, label = "Number"))
hist_n.fill(lep_n)

hist_n.plot(histtype = "fill")
plt.title("Lepton counts per event for multiple datasets")
plt.show()
```

### Over to you


__6)__ Display multiple histograms for lepton number on the same plot.  You'll need the below files:
- 4 leptons - https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363490.llll.4lep.root
- 3 leptons - https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363491.lllv.1largeRjet1lep.root
- 2 leptons - https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363492.llvv.1largeRjet1lep.root
- 1 lepton - https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363493.lvvv.1largeRjet1lep.root


<details>
    <summary>Click here for hint 1: </summary>
        You'll need to access the TTree data for lepton number 4 separate times, 1 for each dataset.
</details>


<details>
    <summary>Click here for hint 2: </summary>
        Think about the bin numbers and boundaries for your axis, and remember that we have 4 datasets now when generating the category axis.
</details>


<details>
    <summary>Click here for hint 3: </summary>
        You'll need to fill your template histogram 4 times.
</details>

```python
### Repeat for each root file
tr1 = uproot.open(###)
lep_n1 = tr1[###].array(###)

### Repeat 4 times

ax = hist.axis.Regular(###)
cax = hist.axis.StrCategory([###], name = ###)
full_hist = Hist(###, ###)

full_hist.fill(###, c = ###)
### Repeat 4 times

s = full_hist.stack(###)
s.###
plt.title(###)
plt.###
plt.###
```

<details>
    <summary>Answer: </summary>
        
    tr1 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363490.llll.4lep.root:mini")
    lep_n1 = tr1["lep_n"].array(library = "np")
    
    tr2 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363491.lllv.1largeRjet1lep.root:mini")
    lep_n2 = tr2["lep_n"].array(library = "np")
    
    tr3 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363492.llvv.1largeRjet1lep.root:mini")
    lep_n3 = tr3["lep_n"].array(library = "np")
    
    tr4 = uproot.open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1largeRjet1lep/MC/mc_363493.lvvv.1largeRjet1lep.root:mini")
    lep_n4 = tr4["lep_n"].array(library = "np")

    ax = hist.axis.Regular(5, -0.5, 5.5, flow=False, name = "Number of leptons")
    cax = hist.axis.StrCategory(["4l", "3l1v", "2l2v", "1l3v"], name = "c")
    full_hist = Hist(ax, cax)
    
    full_hist.fill(lep_n1, c = "4l")
    full_hist.fill(lep_n2, c = "3l1v")
    full_hist.fill(lep_n3, c = "2l2v")
    full_hist.fill(lep_n4, c = "1l3v")
    
    s = full_hist.stack("c")
    s.plot()
    plt.title("Lepton counts per event for multiple datasets")
    plt.legend()
    plt.show()
</details>

---


## Step 5: Normalising histograms <a name="5."></a>


Often, we are more interested in the __proportions__ of our histogram than the absolute number of events it contains (which can change depending on what dataset you use).  Our final step will be to rescale the y-axis of our histogram to that the histogram's total is equal to 1. This is called __normalisation__.


Firstly, we must extract the bin values (heights) as an array, which can be done with the `.values` function.

```python
arr1 = hist1.values()
```

We use the `.sum()` function on our array of bin values to sum the values it contains, then create a new array containing each of the original bin values divided by the sum.

```python
arr2 = arr1/arr1.sum()
```

Let's make a new template histogram:

```python
hist3 = Hist(hist.axis.Regular(5, -0.5, 4.5, flow=False, label = "Number of leptons"))
```

Now we assign our normalised bin values to the original bin values.  Here, we use the length of our `values()` array to refer to the index - simply remove 1 from the full length to refer to the final value, as typical of Python indexing.

```python
binsize = hist1.values()
uplim = len(binsize)-1
hist3[0:uplim] = arr2[0:uplim]
```

Let's see what we get!

```python
hist3.plot(histtype="fill")
plt.show()
```

Now let's show that this is normalised - we've already used the function required to do this!

```python
print(hist3.sum())
```

### Over to you

__6)__ Normalise your histogram and redraw it.


<details>
    <summary>Click here for hint 1: </summary>
        Use .values() to access the height of each bar in the histogram.
</details>


<details>
    <summary>Click here for hint 2: </summary>
        Use .sum to find the sum of these heights - you'll need to divide each bar's height by the sum.
</details>


<details>
    <summary>Click here for hint 3: </summary>
        Redraw your histogram and assign new values to each bin.
</details>

```python
heights = my_hist.###
norm_heights = ###/heights.###
new_hist = Hist(hist.axis.Regular(###, ###, ###, label = ###))
new_hist[###] = norm_heights[###]
new_hist.###
plt.###
```

<details>
    <summary>Answer: </summary>
        
    heights = my_hist.values()
    norm_heights = heights/heights.sum()
    new_hist = Hist(hist.axis.Regular(5, -0.5, 4.5, label = "Number of jets"))
    new_hist[0:4] = norm_heights[0:4]
    new_hist.plot()
    plt.show()
</details>

---


## Optional extra exercises / 'Do your own project' ideas  <a name="6."></a>

> [!NOTE]
> When completing these execises, it is recommended to copy/paste any code you're reusing from above into new cells, to keep the example available for reference.
> [!END]
    
New cells can be added above using `esc` + `a`, below using `esc` + `b`, or using the `Insert` tab at the top of the page.</div> 


1) Remember how to extract the list of branches from a TTree? Choose a new branch from `my_tree` and repeat steps __4-8__ above to show the distribution of that branch's variable over the dataset.

2) Are there any branches in the tree that you do not understand? List up to 3, then explore the
[ATLAS Open Data Documentation](http://opendata.atlas.cern/release/2020/documentation/datasets/intro.html)
    
3) In the example above we plotted the number of leptons resulting from simulated ('Monte-Carlo'/'MC') collisions with one lepton and one jet at an energy of 13 TeV.

- You might have noticed the number of leptons plotted is not exactly 1 for each event. Why might that be?

<details>
    <summary>Click here for hint 1: </summary>
    What exact process is simulated in this file? Look at the last part of the file path, mc_361106.Zee.1largeRjet1lep.root
</details>


<details>
    <summary>Click here for hint 2: </summary>
    Z-->ee is the process simulated here, but one of the electrons is being missed. What could have happened to it?
</details>


Using the instructions for finding new datasets <a href="FindingOpenData.pdf"> here</a>, find a file with two 'final state' leptons and plot the number of leptons. 


<details>
    <summary>Click here for hint 3: </summary>
    Taking our file mc_361106.Zee.1largeRjet1lep.root as an example...
    
    - mc: Means that this file has simulated data
    - 361106: This is a unique identifying number for each file
    - Zee: This is the process being produced
    - 1largeRjet1lep: These are the particles being observed in the simulated detector, in this case 1 large radius jet and 1 lepton
</details>


> [!WARNING]  
> How do the two plots compare?
> Do you understand what all the file names mean?
> [!END]

4) So far, we have only plotted simulated data. 
- Using the instructions above, find the directory containing real collisions with 1 lepton and 1 jet in the final state.
- You might notice that the real data is split across several different files (e.g. data_A.1largeRjet1lep.root). Fill a histogram showing a branch of your choice with ALL the events in the full dataset


<details>
    <summary>Click here for hint 1: </summary>
    Load in each data file and its TTree under a separate name. Create a list containing all your separate trees:
    
    my_trees = [tree1,tree2,tree3,tree4] etc.
</details>


<details>
    <summary>Click here for hint 2: </summary>
    Set up one histogram as usual
</details>


<details>
    <summary>Click here for hint 3: </summary>
    Add an extra layer to your histogram filling for loop, looping over the events in all of your trees 
    
    for tree in my_trees:
        for event in tree:
            ...
</details>


5) So far we have only shown one histogram at a time. Draw two histograms on the same plot to compare them directly e.g. the `n_lepton` branch for the samples with both 1 and 2 final state leptons


<details>
    <summary>Click here for hint 1: </summary>
    Fill two seprate histograms, but only set up 1 plot.
</details>

---

> [!TIP]
> __Congratulations!__ You've worked with actual LHC data like a real particle physicist!
> [!END]
