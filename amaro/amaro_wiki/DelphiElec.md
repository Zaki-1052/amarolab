# DelphiElec

## Basic use of DelphiElec[edit](</mediawiki/index.php?title=DelphiElec&action=edit&section=1> "Edit section: Basic use of DelphiElec")]

Download the [DelphiElec plugin](</mediawiki/index.php?title=DelphiElec_plugin&action=edit&redlink=1> "DelphiElec plugin \(page does not exist\)"). 

This tutorial can also be found at the [DelphiElec website](<http://amarolab.ics.uci.edu/delphielec.html>)

Note: make sure you have Delphi downloaded and located somewhere in your operating system's environment program path. (In Linux/Unix if you type “which delphi” and there isn't an error then you should be all set) Also make sure that you have the most lately updated .siz and .crg files downloaded to somewhere convenient if you plan to use them in the runs (though they aren't mandatory when the charge values exist in the loaded files, for instance: .prmtop and .psf files). 

First you will need to [File:delphielec_tutorial.tgz download the tutorial files] 

Then unpack them with this command: 
    
    
    tar -xfz delphielec_tutorial.tgz

## Running DelphiElec on a single-frame molecule[edit](</mediawiki/index.php?title=DelphiElec&action=edit&section=2> "Edit section: Running DelphiElec on a single-frame molecule")]

### Loading the molecule[edit](</mediawiki/index.php?title=DelphiElec&action=edit&section=3> "Edit section: Loading the molecule")]

  1. On the VMD main window, go to File -> New Molecule
  2. The “Molecule File Browser” window will appear. Under the “Load Files for:” list box, select “New Molecule”
  3. Click “Browse...”
  4. Navigate to “.../cpaf.pdb” Click “OK”
  5. In the Molecule File Browser, Click “Load”



### Start the Delphi run[edit](</mediawiki/index.php?title=DelphiElec&action=edit&section=4> "Edit section: Start the Delphi run")]

  1. In the VMD Main window, select Extensions -> Analysis -> DelphiElec. The DelphiElec plugin window will appear.
  2. Under the option box “Select molecule for Delphi run:” select “0:cpaf.pdb”
  3. In the “Selection” textbox, change the value to “protein”
  4. In the “Write to Output” textbox, change the value to “struct_cpaf.cube”
  5. Make sure the “Load into VMD when finished” option is selected.
  6. Go to the menubar “Edit” -> “Input File”. The Edit Delphi input File window will appear.
  7. Click the button “Load Template Param. File”
  8. Navigate to the file “.../param.in”. Click “Open”
  9. The “Size File” and “Charge File” fields must point to the proper .siz and .crg parameter files that is included in this tutorial or may be downloaded at Clemson's Website: <http://www.ces.clemson.edu/compbio/delphi.html>
  10. Click “OK” to close the Edit Delphi Input File window
  11. Click the “Run Delphi” button. 



Note: This may take several minutes to complete. 

### Examine the results[edit](</mediawiki/index.php?title=DelphiElec&action=edit&section=5> "Edit section: Examine the results")]

Once finished, examine the results of the run: 

  1. Try changing the “Isovalue” slider in the Graphical Representations window under the “Draw style” tab\\\
  2. Try changing the Drawing Method listbox to another value: such as “Volume Slice” or “Field Lines”\\\
  3. Try creating a positive and negative representation of the charge maps by clicking the “Create Rep” button in the Graphical Representations window and changing the isovalue slider to a positive number, and the isovalue of the first representation to a negative number.\\\



## Running DelphiElec on a trajectory[edit](</mediawiki/index.php?title=DelphiElec&action=edit&section=6> "Edit section: Running DelphiElec on a trajectory")]

### Loading a trajectory[edit](</mediawiki/index.php?title=DelphiElec&action=edit&section=7> "Edit section: Loading a trajectory")]

  1. On the VMD main window, go to File -> New Molecule
  2. The “Molecule File Browser” window will appear. Under the “Load Files for:” list box, select “New Molecule”
  3. Click “Browse...”
  4. Navigate to “.../cpaf.prmtop” Click “OK”
  5. In the Molecule File Browser, click “Load”
  6. Under the “Load Files for:” list box, select “cpaf.prmtop”
  7. Click “Browse...”
  8. Navigate to “.../cpaf.dcd” Click “OK”. The trajectory will begin to load



### Align the molecule[edit](</mediawiki/index.php?title=DelphiElec&action=edit&section=8> "Edit section: Align the molecule")]

  1. In the VMD Main window, select Extensions -> Analysis -> RMSD Trajectory Tool. The RMSD Trajectory window will appear.
  2. Make sure the text in the top left corner says “protein”
  3. Below that, select the “Backbone” checkbox
  4. Make sure the checkbox labelled “Trajectory” is selected, with Frame ref set to “0”
  5. Click the “Align” button to align every frame of the protein to the first frame.



### Start the Delphi run[edit](</mediawiki/index.php?title=DelphiElec&action=edit&section=9> "Edit section: Start the Delphi run")]

1\. In the VMD Main window, select Extensions -> Analysis -> DelphiElec. The DelphiElec plugin window will appear.   
2\. Under the option box “Select molecule for Delphi run:” select “1:cpaf.prmtop”   
3\. In the “Selection” textbox, leave the value at “protein”   
4\. In the “Write to Output” textbox, change the value to “traj_cpaf.cube”   
5\. Deselect the “Load into VMD when finished” option, and instead select “Load first frame colored by charge”.   
6\. Go to the menubar “Edit” -> “Input File”. The Edit Delphi Input File window will appear.   
7\. Click the button “Load Template Param. File”   
8\. Navigate to the file “.../param.in”. Click “Open”   
9\. As before, the “Size File” and “Charge File” fields must point to the proper .siz and .crg parameter files that came with your Delphi package or may be downloaded at Clemson's Website: <http://www.ces.clemson.edu/compbio/delphi.html>   
10\. Click “OK” to close the Edit Delphi Input File window   


Note: The trajectory provided in this tutorial has 100 frames, so the entire run will probably take 100 times longer than the single frame calculation done in the previous section: potentially amounting to hours or days. The results of a completed run of this tutorial's trajectory has been provided in the tutorial files. 

11\. If you would like to perform the calculation yourself, click the “Run Delphi” button. 

Otherwise - 

11\. In the VMD main window, go to: File -> New Molecule   
12\. The “Molecule File Browser” window will appear. Under the “Load Files for:” list box, select “New Molecule”   
13\. Click “Browse..."   
14\. Navigate to “.../cpaf_traj.cube” Click OK   
15\. In the Molecule File Browser, click “Load"   
16\. In the VMD Representations window, under the “Drawing method” tab, select “surf”   
17\. In the VMD Representations window, under the “Coloring method” tab, select “volume”   
18\. Zoom out your view so you can see the whole molecule. 

## Examine the Results:[edit](</mediawiki/index.php?title=DelphiElec&action=edit&section=10> "Edit section: Examine the Results:")]

  1. The color differences are very faint. To fix that, go to the Trajectory tab in the Graphical Representations window.\\\
  2. Change the values in the two “Color Scale Data Range” boxes to numbers closer to zero. -/+10 should suffice for this case.\\\



#### Troubleshooting:[edit](</mediawiki/index.php?title=DelphiElec&action=edit&section=11> "Edit section: Troubleshooting:")]

If you recieve an error asking you to “Specify the location for Delphi”, then you must manually enter the location of Delphi by going to “Edit” -> “Settings...”. Then specify the proper path name in the “Delphi Directory” text box. 

If you get errors to the effect of “Missing charge parameter file” or “Missing size parameter file”, keep in mind that both of these must be specified or else neither. And in cases where VMD cannot read charge or radius information directly from the loaded molecule file (such as a PDB file), both of these parameter files must be specified in the “Input File” window.
