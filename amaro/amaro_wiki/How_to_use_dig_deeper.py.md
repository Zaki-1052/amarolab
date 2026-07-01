# How to use dig deeper.py

The program 'dig_deeper.py' is intended to provide a starting structure for a deeper milestone's umbrella stage based on the ending point of a shallower milestone's forward stage. 

Run the dig_deeper script without any arguments to see usage instructions: 
    
    
    python dig_deeper.py 
    

There are three main options for dig_deeper.py: 

### First[edit](</mediawiki/index.php?title=How_to_use_dig_deeper.py&action=edit&section=1> "Edit section: First")]

**first** : The last frame of the first forward trajectory is used to create the starting structure for the deeper milestone. This option is not recommended because it is extracted from an early point in the shallower milestone's umbrella stage. 

sample command: 
    
    
    python dig_deeper.py 10 ~/hsp90_gdm/seekr_calc.pickle first
    

This command runs on milestone 10 (shallower) in order to populate milestone 9 (deeper). Notice that the SEEKR pickle file must be provided, and also the 'first' keyword. 

### Last[edit](</mediawiki/index.php?title=How_to_use_dig_deeper.py&action=edit&section=2> "Edit section: Last")]

**last** : The last frame of the last forward trajectory is used to create the starting structure for the deeper milestone. This option is recommended only if a crystal structure of the holo bound state of the ligand into the protein is not available. Because even though this option takes a frame from a time when the shallower milestone's umbrella stage has most likely equilibrated, there is a likelihood that a conformation will be sampled that is not part of the binding pathway, and may cause yet deeper milestones to sample conformations that are not conducive to binding. Of course, with sufficient sampling in the umbrella stage, this would not be a problem, but sampling may not be sufficient in all cases. The next option: 'similar' is recommended if a crystal structure is available. 

sample command: 
    
    
    python dig_deeper.py 10 ~/hsp90_gdm/seekr_calc.pickle last
    

This command runs on milestone 10 (shallower) in order to populate milestone 9 (deeper). Notice that the SEEKR pickle file must be provided, and also the 'last' keyword. 

### Similar[edit](</mediawiki/index.php?title=How_to_use_dig_deeper.py&action=edit&section=3> "Edit section: Similar")]

**similar** : The last frame of the forward trajectory that most closely resembles the crystal structure is used to create the starting structure for the deeper milestone. This option is recommended if a crystal structure is available. This option requires additional .parm7 and .rst7 files for the holo structure in order to function. 

sample command: 
    
    
    python dig_deeper.py 10 ~/hsp90_gdm/seekr_calc.pickle similar ~/hsp90/holo_native/holo.parm7 ~/hsp90/holo_native/holo.rst7 GDM
    

The previous command runs on milestone 10 (shallower) in order to populate milestone 9 (deeper). Notice that the SEEKR pickle file must be provided as an argument, and also the 'similar' keyword. Beyond that, the .parm7 and .rst7 files are listed, and lastly the residue name (resname) of the ligand itself. 

Note that the 'similar' option takes awhile (several minutes).
