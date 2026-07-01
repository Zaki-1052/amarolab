# CYP Analyses

## Preparing Files for Analysis[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=1> "Edit section: Preparing Files for Analysis")]

You will want to move or copy your system .pdb file, parameter files, and .dcd files into a new directory 

### .DCD Files[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=2> "Edit section: .DCD Files")]

If you're running MD with many frames, you may want to concatenate your .dcd files into one large file 

  1. Download the program [CatDCD](<http://www.ks.uiuc.edu/Development/MDTools/catdcd/>)
  2. Move all your .dcd files into a new directory.
  3. Enter the following command: 
         
         PATH TO CATDCD/catdcd -o OUTPUT.dcd INPUT1.dcd INPUT2.dcd INPUT3.dcd etc.

  4. Change "PATH TO CATDCD" to the correct pathway, and make sure you list the input.dcd files **IN ORDER**



## Alpha Carbon RMSD[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=3> "Edit section: Alpha Carbon RMSD")]

### Method 1 - CHARMM[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=4> "Edit section: Method 1 - CHARMM")]

  1. Load your .psf file into VMD, and then load your .dcd file into the .psf.
  2. In the VMD Main Window, click 
         
         Extensions -> Analysis -> RMSD Trajectory Tool 

  3. This should open up the RMSD Trajectory Tool Window. 
     1. _If your Molecule does not appear in the RMSD Trajectory Tool Window, click "Add All" and then delete any unwanted molecules (if any)_.
  4. Under "File" and "Options" is a grey box. If it does not already say "protein", type "protein" into this box.
  5. Under the box, click the white box next to "noh"
  6. Check the box next to "Plot", and if you want to save the RMSD as a .dat file, click "Save to file" next to it.
  7. Hit the "Align" Button, and then hit the "RMSD" Button. 
     1. _This should give you a plot containing the RMSD Data._
  8. Save the file clicking 
         
         File -> Export to PostScript

  9. Save it as _RMSD_graph.dat_.



See [tutorial](<http://www.ks.uiuc.edu/Training/Tutorials/namd/namd-tutorial-unix-html/node11.html#SECTION00047100000000000000%7CNAMD>) for additional information. 

#### Plotting the graph using Matlab[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=5> "Edit section: Plotting the graph using Matlab")]

The following instructions is for plotting two systems. If you're plotting for one system, ignore the command line for variable "b" in #4. 

  1. Open a terminal and type 'module load matlab', then 'matlab.'
  2. Drag the file "RMSD_file.dat" from the box on the left to the command window.
  3. A new window, Import Wizard will show. 
     1. Select 'Space' under 'Select Column Separator' and select '2' under 'Number of the header lines.'
     2. Click 'next', then 'finish'.
  4. In the command window, type in command: 
         
         x = data(:,1); 
    
    
     a = data(:,2);
     b = data(:,3);

  1. In the command window, type in command: 
         
         plot(x,a,x,b);

  2. Your graph should be shown in a separated window.
  3. Using the labeling tools under "Insert" to label the graph.



[![Rmsd time raw.jpg](/mediawiki/images/3/3d/Rmsd_time_raw.jpg)](</mediawiki/index.php/File:Rmsd_time_raw.jpg>)

#### (Optional) Smoothen the graph[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=6> "Edit section: \(Optional\) Smoothen the graph")]

If you're only plotting for a single system, ignore variable "d" in the following instructions. 

  1. In the command window, type in command: 
         
         c = smooth(a,20);d = smooth(b,20) 

  2. select both "c" and "d" and click on the triangle and select "Plot as multiple series."
  3. Your graph should be shown in a separated window.
  4. Using the labeling tools under "Insert" to label the graph.



[![Rmsd time.jpg](/mediawiki/images/1/17/Rmsd_time.jpg)](</mediawiki/index.php/File:Rmsd_time.jpg>)

## RMSF Per Residue[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=7> "Edit section: RMSF Per Residue")]

### Method 1 - CHARMM & VMD[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=8> "Edit section: Method 1 - CHARMM & VMD")]

  1. Load your .psf file into VMD and load your .dcd file into your .psf 
  2. Save the following file as FILENAME.tcl 
    
    set outname 	 rmsf.dat
     set firstresid 	30   
     set lastresid 	490  
     set frames	2559 
    
     set outfile [open $outname w]
     for {set i $firstresid} {$i < $lastresid+1} {incr i} {
      set sel [atomselect top "protein and resid $i and noh"]
      set rmsf [measure rmsf $sel first 0 last $frames step 1]
      set sum 0.0
      set den 0.0
      set mass [$sel get mass]
      set j 0
      foreach val $rmsf {
        set mt [lindex $mass $j]
        set sum [expr $sum+$mt*$val]
        set den [expr $den+$mt]
        incr j
      } 
      set sum [expr $sum/$den]
      puts $outfile "[expr {$i}] $sum"
     }
     close $outfile 

  3. Make the following edits: 
     1. Replace **30** next to "firstresid" with the first resid of your protein 
     2. Replace **490** next to "lastresid" with the last resid of your protein 
     3. Replace **2559** next to "frames" with the number of frames in your trajectory **_Minus 1_**
        1. ### _If you had 4400 frames, you would put 4399, etc.)_
  4. Load your system .pdb and .psf files into VMD and open the TK Console 
  5. Set the top "T" selection to the system you want to compute 
  6. Enter the following command in the TK Console: 
         
         source FILENAME.tcl




This should give you a .dat output file, which can be exported and graphed in Matlab. 

### Method 2 - Ptraj[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=9> "Edit section: Method 2 - Ptraj")]

Use ptraj in AMBER10 to generate the RMSF v.s. Residue Graph: 

  * Copy the following into a _*Ptraj_script.txt_ file and make necessary changes (has a * next to it) accordingly 


    
    
    #Ptraj RMSF script
       trajin *tot.dcd 1 *500 1                #Input the trajectory file *.dcd here, followed by the number of first frame, last frame,and stride. 
                                               #If there is more than one .dcd file, copy the line above and paste it in this line.
       reference *../alignsptraj/BKalign.pdb   #This is the reference *.pdb file.
       strip !:*1-1509                         #The residue number of the protein. 
    
       #backbone aligned 
       rms reference :*1-1509@CA,C,N,O         #The residue number of the protein. 
       atomicfluct out *RMSF_backbone.txt byres #Name for the output file(Backbone).
      
       #every atom aligned
       rms reference :1-*1509                  #The residue number of the protein.
       atomicfluct out *RMSF_all.txt byres     #Name for the output file(All).
    

  * To run the file, enter 
        
        *ptraj_something.prmtop < *Ptraj_script.txt" 

  * A new file named *_Ptraj_script.txt_ will be generated in the local directory
  * Open this *_Ptraj_script.txt_ file in Microsoft Excel spread sheet to make the graph



### Method 3 - GROMOS (g_rmsf)[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=10> "Edit section: Method 3 - GROMOS \(g rmsf\)")]

  * Use the trajectory.pdb and first_frame.pdb from [gromos_clustering](</mediawiki/index.php/Gromos_clustering> "Gromos clustering").


  * Load the GROMOS module by typing


    
    
    module load gromacs
    

  * Then run g_rmsf by typing


    
    
    g_rmsf -f trajectory.pdb -s first_frame.pdb -ox bfactors.pdb -o rmsf.xvg -res 
    

  * The PDB file bfactors.pdb contains the B-factors of each atom written into the average coordinates. Replacing "-ox bfactors.pdb" with "-oq bfactors.pdb -q input.pdb" will write the B-factors into input.pdb and create the output bfactors.pdb. 



**The RMSF of each residue will be in nanometers, not Ångstroms. Convert nanometers to Ångstroms by multiplying it by 10.**

#### RMSF Graph: Using Microsoft Excel[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=11> "Edit section: RMSF Graph: Using Microsoft Excel")]

#### RMSF Graph: Using Matlab[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=12> "Edit section: RMSF Graph: Using Matlab")]

#### RMSF in VMD: Visualize The Fluctuation[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=13> "Edit section: RMSF in VMD: Visualize The Fluctuation")]

  * Open VMD and click 
        
        load data into the molecule

under 
        
        file

  * Select the *_Ptraj_script.txt_
  * Invert the color by going to _Graphic_ -_Colors_
  * Click on _Color Scale_ tab and choose _BWR_. By doing this



## RMSD Based Clustering[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=14> "Edit section: RMSD Based Clustering")]

Our Clustering Analysis primarily focuses on the Active Site and f-g Loop 

### GROMOS[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=15> "Edit section: GROMOS")]

See [GROMOS Clustering](<http://amarolab.ics.uci.edu/wiki/doku.php/gromos_clustering>)

  * You may choose to align the molecule by the entire protein or select certain residues. 
    * _Active site residues, certain helices, etc._


  * For creating "trajectory.pdb", we chose to use a stride of 4.
  * For the **atom selection** , we have found another method.
  * After you finish the step that creates "first_frame.pdb",load first_frame.pdb back into VMD.
  * Open the TK Console and select the residues you want to analyze.



**_Example:_**

  * If you wanted to analyze a helix with residues 200-220,your selection would look like this:
  * In TK Console:


    
    
      set sel [atomselect top "resid 200 to 220 and protein"]
      $sel get index
    

  * This should generate a list of atom indices.
  * Copy and paste this output into "selection.ndx" and follow the steps on [GROMOS Clustering](<http://amarolab.ics.uci.edu/wiki/doku.php/gromos_clustering>) from there.


  * For the RMSD cutoff, we found 0.175 to be a good value.


  * The GROMOS Clustering page recommends splitting the active site .pdb into several single-frame .pdb files, however, you may want to save individual frames straight from the VMD Main Window Instead (this is useful if you are analyzing clusters of certain residues as opposed to the entire protein). 
    * _This is done by simply right-clicking the .psf/.dcd molecule loaded into VMD, selecting "save coordinates" and changing the first and last frames to the frame you would like to save._



**_IMPORTANT_** If you are using the middle RMSD for your analysis, GROMACS lists starting from 0, where VMD starts from 1. 

**_Example_** If your middle frames were 1341, 241, 356, and 4219, they would correspond to frames 1342, 242, 357, and 4220 in VMD respectively. 

##### GROMOS Online[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=16> "Edit section: GROMOS Online")]

  1. Write down all the residues that are near the active or binding site.
  2. Take a picture of the lining residues.
  3. Clustering. See [GROMOS Cluster](<http://kryptonite.nbcr.net/opal2/dashboard?command=serviceList>) and select GROMOS Clustering. For the files that are required for submission. See [gromos_clustering] for the trajectory file and the active site file.
  4. Upload the trajectory pdb file and the active site pdb file.
  5. Start the RMSD cutoff with 0.125.
  6. Repeat the submission job with different cutoff values till 0.200 with an increment of 0.010 at a time. (e.g. 0.125,0.135,0.145,0.155,0.165,0.175,0.185,0.195,0.200 for each submission job)
  7. Make a graph with Number of Clusters v.s. RMSD cutoff that looks like [this](<http://amarolab.ics.uci.edu/wiki/lib/exe/detail.php/clustering_graph.png?id=gromos_clustering>).
  8. Determine the best cutoff value.



For additional clustering method, see [gromos_clustering](</mediawiki/index.php/Gromos_clustering> "Gromos clustering")

##### Clustering Analysis[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=17> "Edit section: Clustering Analysis")]

  1. Determine the volume of the binding site.
  2. Determine major structural differences at binding site.
  3. Determine the residues that have the greatest RMSD value.
  4. Determine the structural rearrangement in the membrane region.
  5. Determine the structural differences in the substrate channel.
  6. Determine whether the substrate channel in membrane-bound and in water.



## Hydration Analysis[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=18> "Edit section: Hydration Analysis")]

### Method 1 - CHARMM[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=19> "Edit section: Method 1 - CHARMM")]

  1. Load your .psf file and .dcd file into VMD.
  2. Using the RMSD Trajectory Tool, Align the molecule to **protein**.
  3. Go to 
         
         "Extensions -> Analysis -> VolMap Tool" 

  4. Change "Selection" to water if it isn't already done so.
  5. Select the correct molecule and change "volmap type" to occupancy.
  6. Check the box next to "compute for all frames, and combine using:" and select "avg".
  7. Change Output Destination.
  8. Click "Write to file" and choose a filename.
  9. Hit "Create Map".
  10. Load the new .dx file into VMD as a new molecule.
  11. Under "Graphical Representations" change "Draw" to Solid Surface.
  12. Adjust the Isovalue bar to get the most accurate representation. 
     1. _the Isovalue tells you where water is at what percent of the time, so if you change the value to .9, it will show where water is 90% of the trajectory_



## Volume Analysis[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=20> "Edit section: Volume Analysis")]

### Method 1 - FPocket[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=21> "Edit section: Method 1 - FPocket")]

_This should be done after clustering analysis_

  * Download [fpocket2](<http://fpocket.sourceforge.net/>)
    * _(Read the instructions on how to compile/install it in INSTALL.txt)_
    * Follow the steps below to unzip the file and install fpocket2.


    
    
    tar -xzf fpocket-src-1.0.tgz
    
    
    cd fpocket-src-1.0
    
    
    make
    
    
    make test
    
    
    make install

  * Read fpocket [manual](<http://fpocket.sourceforge.net/manual_fpocket2.pdf>)
  * Copy your .pdb files obtained from clustering analysis into a new directory
  * Enter the following command: 
        
        PATH TO FPOCKET/fpocket -f CLUSTERFRAME.pdb 

  * Change "PATH TO FPOCKET" to the correct pathway, and enter the correct .pdb to be analyzed.



### Method 2 - Povme[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=22> "Edit section: Method 2 - Povme")]

See <http://www.nbcr.net/POVME/#>

## Heme-Membrane Orientation[edit](</mediawiki/index.php?title=CYP_Analyses&action=edit&section=23> "Edit section: Heme-Membrane Orientation")]

To calculate the angle between the heme and membrane plane (with normal (0,0,1)) the following Tcl script can be used in VMD, in this example it is processing the first 2500 frames 
    
    
    for { set i 0 } { $i < 2500 } { incr i } {
    set sel1 [atomselect top "heme and name NA" frame $i]
    set sel2 [atomselect top "heme and name NB" frame $i]
    set sel3 [atomselect top "heme and name NC" frame $i]
    set x [measure center $sel1]
    set y [measure center $sel2]
    set z [measure center $sel3]
    set q [vecsub $x $y]
    set r [vecsub $y $z]
    set T [veccross $q $r]
    set a [vecnorm $T]
    set dp [lindex $a 2]
    set v [expr 180.0*acos($dp)/3.14159]
    puts $i,$v
    }
    

The output is lines on the screen with format "frame_number,angle_in_degrees"
