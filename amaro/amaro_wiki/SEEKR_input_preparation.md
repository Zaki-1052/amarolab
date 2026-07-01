# SEEKR input preparation

This page will walk you through preparation of your SEEKR script. 

First you want to pull the template from git. To do this, in an open terminal type: 
    
    
    git pull origin master
    

This should give you access to the template script. Open PREP_SCRIPT_TEMPLATE with gedit. Make a copy of the script for your simulation. Once you have made a copy you can begin preparing your simulation. Read through the template and input the information specific to your simulation indicated by five hashtags. 

  
You will want to set the temperature of your simulation. Most simulations run at 298.15 kelvin, but it may be different depending on your system. 

  
For the project information you will want to name your project and identify where it is located. If you want to run the MD and/or the BD stage set the boolean variable to True, if not set them to False. 

  
Next you are going to identify the indices. If you know the residue IDs, you can find the indices using the VMD TkConsole. 

For example: 
    
    
    set site [atomselect 0 "name CA and resid 35 42 77 91 122 168 169"]
    $site get index
    

This should return the indices. Make sure the number after atomselect indicates the ID of your molecule in VMD. 

If you do not already know the residue IDs, you can find them by identifying the locations on the protein in which the ligand interacts. If you select these locations, you will find the residue name and ID. 

  
For the building information define each thing indicated by five hashtags. There is an example for each item, but your input should be unique to your simulation. 

  
Next you will identify the ions, ion concentrations, ion charges, and ion radii you will use for your simulation. You will get this information from scholarly articles about your system. 

  
To generate milestones you will need to define the coordinates of the origin, which is the center of the indices, list the radii of the spherical milestones, and define the coordinates of two sequential vectors pointing outwards from the center. To find the coordinates of the origin, assuming you earlier define site as the alpha carbons and residues, into your TkConsole type: 
    
    
    measure center $site
    

This will return the coordinates of the origin. After this you will list the radii of the spherical milestones you will be using for your simulation. To find the coordinates of two sequential vectors pointing outwards from the center follow the directions here: <https://wiki.amaro.ucsd.edu/mediawiki/index.php/Drawing_vectors>

  
Next you will define a leap template file. You can find an example leap script here: <https://wiki.amaro.ucsd.edu/mediawiki/index.php/Example_leap_script>

  
Finally, you will define the solvated box vectors in angstroms. You can find these values from the last row of an .inpcrd or .rst7 file from your apo simulation. From these values you can calculate the vectors needed for the box vector list. You can find these calculations here: <https://wiki.amaro.ucsd.edu/mediawiki/index.php/Build_receptor_from_PDB> . **Make sure that the parm.box vectors are in angstroms and the box vector list is in nanometers.**

Read through the script again and make sure all fields that needed to be edited for your simulation are complete.
