# DNA Analysis - Curves+

DNA Analysis can be easily done with Curves+ suite. WEB: <https://bisi.ibcp.fr/tools/curves_plus/>

Curves+ itself can only analyze one single frame, but with the help of Canal (a module from the Curves+ suite), we can analyze DNA from trajectories. 

# Preparing Inputs[edit](</mediawiki/index.php?title=DNA_Analysis_-_Curves%2B&action=edit&section=1> "Edit section: Preparing Inputs")]

First, we need to extract the trajectories contain only the DNA. We can do that in cpptraj. 

Here is an sample script, given that the trajectory files and the topology file are in one directory above our current folder: 
    
    
    #load amber prmtop file
    parm ../p53_tet_p21_N.top     
    #load trajectory files                                                  
    trajin ../p21_stride_5_prod1_109ns.dcd                                    
    trajin ../p21_stride_5_prod2_109ns.dcd                                           
    trajin ../p21_stride_5_prod3_109ns.dcd    
    #align the system using a selected set of residues from the protein                    
    rms first :89-291,483-685,877-1079,1271-1473@CA  
    #strip everything except the DNA (residue# 1577-1798)                  
    strip !:1577-1708      
    #generate a trajectory output file called p21_DNA.mdcrd with only the DNA                                                                       
    trajout p21_DNA.mdcrd trajectory                                     
    go
    

We shall save this sample script in a text format. For convenient, we call the above sample script createpdb.traj. 

Then, we run the sample script in a terminal by typing 
    
    
    cpptraj -i createpdb.traj
    

A trajectory named p21_DNA.mdcrd then appear in the current directory. Even though this is the file format needed, Curves+ actually do not recognize the .mdcrd extension. 

Thus, we want to change the extension from .mdcrd to .trj (a file format and extension that Curves+ read). 
    
    
    mv p21_DNA.mdcrd p21_DNA.trj
    

Afterwards, we want a DNA topology to go with the trajectory. We create it using parmEd from the Amber suite. 

We will need to write a small input file for parmEd and here is a sample script: 
    
    
    strip !:1577-1708
    parmout p21_DNA.prmtop
    

Save the input script and let's call it createtop.parmEd 

We run the script using the following command in a terminal assuming that the p53_tet_p21_N.top file is in a directory above the current directory: 
    
    
    /soft/linux/amber12/bin/parmed.py ../p53_tet_p21_N.top createtop.parmEd
    

After parmEd is finished, you will find a prmtop file called p21_DNA.prmtop in your current directory. 

# Running Curves+[edit](</mediawiki/index.php?title=DNA_Analysis_-_Curves%2B&action=edit&section=2> "Edit section: Running Curves+")]

Canal requires inputs from Curves+. There is no input script to run Curves+, all the commands will need to be typed in a terminal. 

Here are the sample commands to run Curves+ for the p21_DNA.trj input trajectories we created earlier: 
    
    
    Cur+ <<!
     &inp file = p21_DNA.trj, ftop = p21_DNA.prmtop, lis = Results_p21_DNA, 
     lib = /soft/curves/standard
     &end
    2 1 -1 0 0
    1:64
    130:67
    !
    

_**Cur+ <<!**_ called Curves+, 

_**& inp**_ signal the start of input command, 

_**file**_ specifies the name of the input file including extension, 

_**ftop**_ is a parameter for listing the Amber topology file that matches the input trajectory. Extension is needed, and only .prmtop is recognized. 

_**lis**_ specifies the output name. 

_**lib**_ is required for the calculation and /soft/curves/standard is the path that leads to the library in the Amarolab machines. 

_**& end**_ signals the end of the input command 

_**2 1 -1 0 0**_ specifics the 5' to 3' and 3' to 5' DNA direction. You probably won't need to change it. 

_**1:64**_ is the residue number from a single stranded of complementary DNA starting from 5' to 3'. 

_**128:65**_ is the residue numbers from the other single stranded DNA starting from 5' to 3'. 

_**!**_ signals that you are done with command input and Curves+ can start the calculation. 

After the calculations are finished, in the current directory, you should see two files with extensions of .cda and .lis. In our example above, these two files are called Results_p21_DNA.cda and Results_p21_DNA.lis. 

# Running Canal[edit](</mediawiki/index.php?title=DNA_Analysis_-_Curves%2B&action=edit&section=3> "Edit section: Running Canal")]

Finally, we are ready to run Canal to analyze the DNA trajectories. Canal output generates a list of different DNA parameters such as shear, stretch, and xdisp, etc. and their average and standard deviations. 

Same as running Curves+, there is no input script needed to run Canal. We will type in every commands in a terminal. 

Here are the sample command: 
    
    
    canal <<!
     &inp lis=Canal_p21_DNA, seq=AGGAACATGTCCCAACATGTTGAGA, lev1=26, lev2=64,
     &end
    Results_p21_DNA AGGAACATGTCCCAACATAAAGGAACATGTCCCAACATGTTGAGAAATGTCCCAACATGTTGAG
    Results_p21_DNA TCCTTGTACAGGGTTGTATTTCCTTGTACAGGGTTGTACAACTCTTTACAGGGTTGTACAACTC
    !
    

Canal <<! calls Canal 

_**& inp**_ signals the start of input command, 

_**lis**_ specifies the output name. 

_**seq**_ specifies the DNA sequence we would like to analyze. You can list a segment or the entire DNA sequence. 

When the seq parameter is called, Canal search for the sequence. _**Lev1**_ specifies the lower bound of the search and _**lev2**_ sets the upper bound. For example, if lev1 is set at 26 and lev2 is set at 64, Canal will search for sequences, which have more than 26 and less than 64 nucleotides that match seq. 

_**& end**_ signals the end of the input command 

It is required for canal users to specifies the root name of the outputs generated from Curves+ (same name used for lis from Curves+), follows by the list of all the nucleotides. Canal uses the outputs from Curves+ for some further calculations. 

_**!**_ signals that you are done with command input and Canal can start the calculation. 

After the calculation is finished, you should see an output file with the root name you specify in lis. From the above sample command, we input lis = Canal_p21_DNA; therefore, our output is called Canal_p21_DNA.lis. You can view the file using gedit or some word processing software. There are many DNA related parameters Curves+ and Canal analyze from the input trajectories. For more information of what which of the parameters present, you can read through the following links: 

  * <https://en.wikipedia.org/wiki/Nucleic_acid_double_helix#Helix_geometries>
  * <http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2761274/>
  * <http://nar.oxfordjournals.org/content/early/2011/05/10/nar.gkr316.full>
