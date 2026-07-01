# Openeye

To access the OpenEye Software type: 
    
    
    > module load openeye/1.0 
    
    
    > module load openeye/2.0 

Loading both modules will allow for full function of omega2. 
    
    
    > vida 

Vida is the visualization gui for OpenEye. 

Other applications can be run as command line by opening them instead of Vida. 

We have rocs, eon, brood, zap, fred, omega, and sybki. 

You can get help on each command by typing "--help" after each application name, for example: 
    
    
    > rocs --help
    

pdf or html manuals for each tool can be found under each tools’ directory within the openeye directory, for example for rocs: 
    
    
    > cd /pkg/openeye/2.0/docs/rocs/3.1.1
    

You can get more information about each application at <http://eyesopen.com> or look at my comments below: 

ROCS = a tool for searching a ligand database for compounds with shape similarity to your query compound using a Tanamoto cut off; this is a useful supplement or prefilter to docking queries of ligand databases. 

EON = a tool for searching a ligand database for compounds with electrostatic profile similar to your query compound; this is also a useful supplement or prefilter to docking queries of ligand databases. 

I’ve found both ROCS and EON to be used extensively by pharma comp sci groups and I have found them useful. 

FRED = Open Eyes’ docking program; it can be set up in the VIDA gui or as a standalone. 

ZAP = a PB model - electrostatic potential calculation program for proteins; Anthony Nichols’ latest DELPHI 

Szybki = a scoring function, uses MMFF & a variety of solvent models to reoptimize the ligand/protein interaction (post-modeling or docking), uses ZAP electrostatics for active site, etc. See the webpage for more info. None of the target-ligand interactions I tried this on were well predicted by this model but others have found success with this tool. It may be very target specific. 

Omega = ligand conformational search tool; it can be used similarly to Schrodinger’s LigPrep and has become an industry standard. If we find we are using ROCS/EON frequently, perhaps we can run omega on some of our most searched ligand databases and keep it in a shared directory to save on disk space and time! 

Brood = this is a new tool I’ve not tried yet. It searches for fragment replacements in ligands, again based on shape & electrostatics. I went to Geoff Skillman’s talk (the developer) at ACS; let me know if you want additional information. 

Openeye also makes a tool named Vivant which is an alternative to using PyMol during presentations. Vivant can be embedded directly in Powerpoint presentations with molecular views/zooming etc that can be clicked through easily or a mouse can use interactively to change views of the molecule. 

VAF 4Apr2011 

License server: mesalane, /pkg/openeye directory for modules. 

Expiration Date: 23-mar-2012
