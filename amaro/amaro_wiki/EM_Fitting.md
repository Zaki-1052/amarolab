# EM Fitting

# EM density map can be generated from MD trajectories using MDFF[edit](</mediawiki/index.php?title=EM_Fitting&action=edit&section=1> "Edit section: EM density map can be generated from MD trajectories using MDFF")]

We can load our trajectories into vmd. 
    
    
    mol new {/scratch/pieong/p53_fl_NEW/p21/p53_tet_p21_N.top} type {parm7} first 0 last -1 step 1 waitfor 1
    mol addfile {/scratch/pieong/p53_fl_NEW/p21/p21_stride_5_prod1_109ns.dcd} type {dcd} first 0 last -1 step 1 waitfor all
    

Then, in the TK console, type the following to load mdff plugin into VMD 
    
    
    package require mdff
    

After that, you will need to select a set of atoms for the density map calculation 
    
    
    set sel [atomselect top "protein"]
    

Finally, you will type in the following command to generate a density map in .dx output format 
    
    
    mdff sim $sel -o output.dx -res ## -spacing ## -allframes
    

where -o specify the output file location and name, -res is the resolution of the density map, -spacing specify the spacing, and -allframes asks mdff to calculate the density map using all frames. Usually, the purpose of generating a density map is to compare it to experimental results, such as Cryo-EM or negative-stain EM. -res and -spacing, hence, are parameters from the experiments. 

Here is an example of the p21 system. We want to use the density map to compare to a negative-stain EM map with a resolution of 30Å and a spacing of 2.1Å 
    
    
    mdff sim $sel -o /scratch/pieong/p53_fl_new/p21/Analysis_EM/p21_prod1_density_map.dx -res 30 -spacing 2.1 -allframes
